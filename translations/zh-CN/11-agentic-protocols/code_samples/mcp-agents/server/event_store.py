#!/usr/bin/env python3
"""
MCP 会话恢复的事件存储实现

此模块提供事件存储实现，通过在客户端重新连接后存储和重放事件来实现 MCP 会话恢复。
"""

import asyncio
import logging
import sqlite3
from typing import Optional

from pydantic import TypeAdapter

from mcp.server.streamable_http import (
    EventCallback,
    EventId,
    EventMessage,
    EventStore,
    StreamId,
)
from mcp.types import JSONRPCMessage

logger = logging.getLogger(__name__)


class SimpleEventStore(EventStore):
    """简单的内存事件存储，用于测试恢复功能。"""

    def __init__(self):
        self._events: list[tuple[StreamId, EventId, JSONRPCMessage]] = []
        self._event_id_counter = 0
        logger.info("SimpleEventStore 已初始化")

    async def store_event(self, stream_id: StreamId, message: JSONRPCMessage) -> EventId:
        """存储事件并返回其 ID。"""
        self._event_id_counter += 1
        event_id = str(self._event_id_counter)
        self._events.append((stream_id, event_id, message))
        logger.info(f"已存储事件 {event_id} 到流 {stream_id}")
        return event_id

    async def replay_events_after(
        self,
        last_event_id: EventId,
        send_callback: EventCallback,
    ) -> StreamId | None:
        """重放指定 ID 之后的事件。"""
        logger.info(f"正在重放 {last_event_id} 之后的事件")
        
        # 查找最后一个事件 ID 的索引
        start_index = None
        for i, (_, event_id, _) in enumerate(self._events):
            if event_id == last_event_id:
                start_index = i + 1
                break

        if start_index is None:
            # 如果未找到事件 ID，则从头开始
            start_index = 0
            logger.info("未找到事件 ID，从头开始")

        stream_id = None
        # 重放事件
        replayed_count = 0
        for _, event_id, message in self._events[start_index:]:
            await send_callback(EventMessage(message, event_id))
            replayed_count += 1
            # 从第一个重放的事件中捕获流 ID
            if stream_id is None and len(self._events) > start_index:
                stream_id = self._events[start_index][0]

        logger.info(f"已重放 {replayed_count} 个事件，stream_id: {stream_id}")
        return stream_id

    def get_event_count(self) -> int:
        """获取存储的事件总数。"""
        return len(self._events)

    def clear_events(self) -> None:
        """清除所有存储的事件。"""
        self._events.clear()
        self._event_id_counter = 0
        logger.info("事件存储已清除")


class PersistentEventStore(EventStore):
    """
    使用 SQLite 将事件持久化到磁盘的事件存储。
    """
    
    def __init__(self, storage_path: str = "events.db") -> None:
        self.storage_path = storage_path
        self._adapter = TypeAdapter(JSONRPCMessage)

        # 使用 check_same_thread=False 以允许从 asyncio 执行器线程访问
        self._conn = sqlite3.connect(self.storage_path, check_same_thread=False)
        self._create_table()
        logger.info(f"PersistentEventStore 已初始化，存储路径: {self.storage_path}")

    def _create_table(self) -> None:
        """如果事件表不存在，则创建它。"""
        cursor = self._conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stream_id TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)
            self._conn.commit()
        except sqlite3.Error:
            logger.exception("在 PersistentEventStore 中创建 'events' 表失败")
            try:
                self._conn.close()
            except Exception:
                logger.exception("表创建错误后关闭 SQLite 连接失败")
            raise
        finally:
            try:
                cursor.close()
            except Exception:
                logger.exception("表创建后关闭 SQLite 游标失败")
    
    async def store_event(self, stream_id: StreamId, message: JSONRPCMessage) -> EventId:
        """存储事件并返回其 ID。"""
        # 将消息序列化为 JSON
        json_str = self._adapter.dump_json(message).decode('utf-8')

        # 在线程池中运行 DB 操作以避免阻塞事件循环
        return await asyncio.to_thread(self._store_event_sync, stream_id, json_str)

    def _store_event_sync(self, stream_id: StreamId, json_str: str) -> EventId:
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO events (stream_id, message) VALUES (?, ?)",
            (stream_id, json_str)
        )
        self._conn.commit()

        event_id = str(cursor.lastrowid)
        logger.info(f"已存储事件 {event_id} 到流 {stream_id}")
        return event_id
    
    async def replay_events_after(
        self,
        last_event_id: EventId,
        send_callback: EventCallback,
    ) -> StreamId | None:
        """重放指定 ID 之后的事件，按最后一个事件的流进行过滤。"""
        logger.info(f"正在重放 {last_event_id} 之后的事件")

        # 在线程池中获取事件
        events_data = await asyncio.to_thread(self._fetch_events_sync, last_event_id)

        if events_data is None:
            logger.warning(f"无法从事件 {last_event_id} 恢复流")
            return None

        stream_id = None
        replayed_count = 0

        for event_id, row_stream_id, message_json in events_data:
            if stream_id is None:
                stream_id = row_stream_id

            try:
                message = self._adapter.validate_json(message_json)
                await send_callback(EventMessage(message, event_id))
                replayed_count += 1
            except Exception as e:
                logger.error(f"反序列化事件 {event_id} 失败: {e}")

        logger.info(f"已为流 {stream_id} 重放 {replayed_count} 个事件")
        return stream_id

    def _fetch_events_sync(self, last_event_id: EventId) -> list[tuple[EventId, StreamId, str]] | None:
        try:
            target_id = int(last_event_id)
        except (ValueError, TypeError):
            logger.warning(f"无效的事件 ID 格式: {last_event_id}")
            return None

        cursor = self._conn.cursor()

        # 1. 从最后一个事件 ID 识别流
        cursor.execute("SELECT stream_id FROM events WHERE id = ?", (target_id,))
        result = cursor.fetchone()

        if not result:
            logger.warning(f"未找到事件 ID {target_id}")
            return None

        stream_id = result[0]

        # 2. 仅获取此流的后续事件
        cursor.execute(
            "SELECT id, stream_id, message FROM events WHERE id > ? AND stream_id = ? ORDER BY id ASC",
            (target_id, stream_id)
        )

        # 将行转换为 (str_id, stream_id, msg_json) 列表
        return [(str(row[0]), row[1], row[2]) for row in cursor.fetchall()]

    def get_event_count(self) -> int:
        """获取存储的事件总数。"""
        cursor = self._conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        result = cursor.fetchone()
        return result[0] if result else 0

    def clear_events(self) -> None:
        """清除所有存储的事件。"""
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM events")
        # 重置自增序列
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='events'")
        self._conn.commit()
        logger.info("事件存储已清除")

    def close(self) -> None:
        """关闭底层 SQLite 连接。"""
        conn = getattr(self, "_conn", None)
        if conn is None:
            return
        try:
            conn.close()
            logger.info("PersistentEventStore 连接已关闭")
        except sqlite3.Error as exc:
            logger.warning("关闭 PersistentEventStore 连接时出错: %s", exc)
        finally:
            self._conn = None

    def __enter__(self) -> "PersistentEventStore":
        """进入与此对象相关的运行时上下文。"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出运行时上下文并关闭连接。"""
        self.close()
