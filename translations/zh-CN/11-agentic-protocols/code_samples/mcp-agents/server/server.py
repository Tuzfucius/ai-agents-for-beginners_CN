#!/usr/bin/env python3
"""
可恢复 MCP 服务器实现

此服务器提供使用事件存储的完整会话恢复功能。
它支持长时间运行的任务，这些任务可以在客户端断开连接后恢复。
"""

import argparse
import asyncio
import logging
import re
from turtle import st
from typing import Optional

import anyio
import uvicorn
from pydantic import AnyUrl
from starlette.applications import Starlette
from starlette.routing import Mount
from pydantic import BaseModel, Field
from mcp.server import Server
from mcp.server.streamable_http import EventStore
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import TextContent, Tool, SamplingMessage

from .event_store import SimpleEventStore

logger = logging.getLogger(__name__)


                            
class PriceConfirmationSchema(BaseModel):
    confirm: bool = Field(description="确认此行程的价格")
    notes: str = Field(default="", description="关于价格的任何附加备注")
                            
class ResumableServer(Server):
    """用于恢复测试的具有长时间运行工具和通知的服务器实现。"""

    def __init__(self, name: str = "resumable_mcp_server"):
        super().__init__(name)
        logger.info(f"ResumableServer '{name}' 已初始化")

        @self.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """列出可用的工具，包括可恢复的工具。"""
            return [
                Tool(
                    name="travel_agent",
                    description="预订旅行行程，包含进度更新和价格确认",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "destination": {
                                "type": "string",
                                "description": "旅行目的地",
                                "default": "Paris"
                            }
                        }
                    },
                ),
                Tool(
                    name="research_agent",
                    description="研究主题，包含进度更新和交互式摘要",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "研究主题",
                                "default": "AI trends"
                            }
                        }
                    },
                ),
                Tool(
                    name="long_running_agent",
                    description="用于测试恢复的长时间运行任务（50步，每步2秒）",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    },
                ),
            ]

        @self.call_tool()
        async def handle_call_tool(name: str, args: dict) -> list[TextContent]:
            """处理工具执行，支持长时间运行任务。"""
            ctx = self.request_context
            logger.info(f"工具调用: {name}，参数: {args}")

            if name == "travel_agent":
                destination = args.get("destination", "Paris")
                logger.info(f"旅行代理：目的地={destination}")
                
                # 简单的旅行预订流程，包含进度更新
                steps = [
                    "正在检查航班...",
                    "查找可用日期...", 
                    "确认价格...",
                    "预订航班..."
                ]
                
                elicitation_result = None
                booking_cancelled = False
                
                for i, step in enumerate(steps):
                    await ctx.session.send_progress_notification(
                        progress_token=ctx.request_id,
                        progress=i * 25,
                        total=100,
                        message=step, 
                        related_request_id=str(ctx.request_id)   
                    )
                    
                    # 在第3步添加引导请求（确认价格）
                    if i == 2:  # "确认价格..."步骤
                        try:
                            elicit_result = await ctx.session.elicit(
                                message=f"请确认您前往 {destination} 的预估价格 $1200",
                                requestedSchema=PriceConfirmationSchema.model_json_schema(),
                                related_request_id=ctx.request_id,
                            )
                            
                            elicitation_result = elicit_result
                            
                            if elicit_result and elicit_result.action == "accept":
                                logger.info(f"用户确认价格：{elicit_result.content}")
                                # 继续预订
                            elif elicit_result and elicit_result.action == "decline":
                                logger.info(f"用户拒绝价格确认：{elicitation_result.content}")
                                booking_cancelled = True
                                # 停止预订流程
                                await ctx.session.send_progress_notification(
                                    progress_token=ctx.request_id,
                                    progress=100,
                                    total=100,
                                    message="预订已被用户取消",
                                    related_request_id= str(ctx.request_id)
                                )
                                break
                            else:
                                logger.info("用户取消了引导")
                                booking_cancelled = True
                                await ctx.session.send_progress_notification(
                                    progress_token=ctx.request_id,
                                    progress=100,
                                    total=100,
                                    message="预订已取消"
                                )
                                break
                                
                        except Exception as e:
                            logger.info(f"引导请求失败（这在测试中是正常的）：{e}")
                            # 无论如何都继续预订作为后备
                    
                    if not booking_cancelled:
                        await anyio.sleep(2)  # 步骤之间固定 0.5 秒延迟
                
                # 根据引导结果生成最终结果
                if booking_cancelled:
                    if elicitation_result and hasattr(elicitation_result, 'content') and elicitation_result.content:
                        notes = elicitation_result.content.get('notes', '未提供原因')
                        result_text = f"❌ 前往 {destination} 的预订已取消。原因：{notes}"
                    else:
                        result_text = f"❌ 前往 {destination} 的预订已取消。"
                else:
                    # 成功预订的最终进度更新
                    await ctx.session.send_progress_notification(
                        progress_token=ctx.request_id,
                        progress=100,
                        total=100,
                        message="行程预订成功"
                    )
                    
                    # 在成功消息中包含确认详情
                    if elicitation_result and elicitation_result.action == "accept" and elicitation_result.content:
                        notes = elicitation_result.content.get('notes', '无附加备注')
                        result_text = f"✅ 行程已成功预订到 {destination}！价格已确认，备注：'{notes}'"
                    else:
                        result_text = f"✅ 行程已成功预订到 {destination}！"

                return [TextContent(type="text", text=result_text)]

            elif name == "research_agent":
                topic = args.get("topic", "AI trends")
                logger.info(f"研究代理：主题={topic}")
                
                # 简单的研究流程，包含进度更新
                steps = [
                    "收集资料...",
                    "分析数据...", 
                    "总结发现...",
                    "完成报告..."
                ]
                
                sampling_summary = None
                
                for i, step in enumerate(steps):
                    await ctx.session.send_progress_notification(
                        progress_token=ctx.request_id,
                        progress=i * 25,
                        total=100,
                        message=step
                    )
                    
                    # 在第3步添加采样请求（总结发现）
                    if i == 2:  # "总结发现..."步骤
                        try:
                            sampling_result = await ctx.session.create_message(
                                messages=[
                                    SamplingMessage(
                                        role="user",
                                        content=TextContent(type="text", text=f"请总结关于以下主题的研究关键发现：{topic}")
                                    )
                                ],
                                max_tokens=100,
                                related_request_id=ctx.request_id,
                            )
                            
                            if sampling_result and sampling_result.content:
                                if sampling_result.content.type == "text":
                                    sampling_summary = sampling_result.content.text
                                    logger.info(f"收到采样摘要：{sampling_summary}")
                                    
                        except Exception as e:
                            logger.info(f"采样请求失败（这在测试中是正常的）：{e}")
                    
                    await anyio.sleep(2)  # 步骤之间固定 0.5 秒延迟
                
                # 最终进度更新
                await ctx.session.send_progress_notification(
                    progress_token=ctx.request_id,
                    progress=100,
                    total=100,
                    message="研究成功完成"
                )

                # 如果有采样摘要则使用，否则使用默认消息
                if sampling_summary:
                    result_text = f"🔍 关于 '{topic}' 的研究成功完成！\n\n📊 关键发现（来自用户输入）：{sampling_summary}"
                else:
                    result_text = f"🔍 关于 '{topic}' 的研究成功完成！"
                
                return [TextContent(type="text", text=result_text)]

            elif name == "long_running_agent":
                # 针对恢复测试优化的固定值
                steps = 50
                duration = 2.0
                logger.info(f"长时间运行代理：{steps} 步，每步 {duration} 秒")
                
                # 发送初始日志消息
                await ctx.session.send_log_message(
                    level="info",
                    data="长时间运行任务已开始",
                    logger="long_running_agent",
                    related_request_id=ctx.request_id,
                )
                
                # 执行长时间运行任务
                for i in range(steps):
                    current_step = i + 1
                    # 使用整数运算避免浮点精度问题
                    progress_percent = (current_step * 100) // steps
                    
                    # 每步发送日志消息
                    await ctx.session.send_log_message(
                        level="info",
                        data=f"正在处理步骤 {current_step}/{steps} ({progress_percent}%)",
                        logger="long_running_agent",
                        related_request_id=ctx.request_id,
                    )
                    
                    # 等待 2 秒
                    await anyio.sleep(duration)
                
                # 发送完成日志消息
                await ctx.session.send_log_message(
                    level="info",
                    data=f"任务成功完成！已在 {steps * duration:.0f} 秒内处理了 {steps} 步。",
                    logger="long_running_agent",
                    related_request_id=ctx.request_id,
                )
                
                # 最终完成消息
                result_text = f"✅ 长时间运行任务成功完成！已在 {steps * duration:.0f} 秒内处理了 {steps} 步。"
                return [TextContent(type="text", text=result_text)]

            else:
                raise ValueError(f"未知工具：{name}")


def create_server_app(event_store: Optional[EventStore] = None) -> Starlette:
    """创建带有可恢复 MCP 服务器的 Starlette 应用程序。"""
    # 创建服务器实例
    server = ResumableServer()

    # 创建安全设置
    security_settings = TransportSecuritySettings(
        allowed_hosts=["127.0.0.1:*", "localhost:*"],
        allowed_origins=["http://127.0.0.1:*", "http://localhost:*"]
    )

    # 创建带有事件存储的会话管理器
    session_manager = StreamableHTTPSessionManager(
        app=server,
        event_store=event_store,
        json_response=False,  # 使用 SSE 流
        security_settings=security_settings,
    )

    # 创建 ASGI 应用程序
    app = Starlette(
        debug=True,
        routes=[
            Mount("/mcp", app=session_manager.handle_request),
        ],
        lifespan=lambda app: session_manager.run(),
    )

    return app


async def run_server(port: int = 8006, with_event_store: bool = True) -> None:
    """运行可恢复 HTTP 服务器。"""
    # 如果请求则创建事件存储
    event_store = SimpleEventStore() if with_event_store else None
    
    # 创建应用程序
    app = create_server_app(event_store)

    # 配置服务器
    config = uvicorn.Config(
        app=app,
        host="127.0.0.1",
        port=port,
        log_level="info",
        limit_concurrency=10,
        timeout_keep_alive=30,
        access_log=True,
    )

    logger.info(f"正在启动可恢复 HTTP MCP 服务器，地址：http://127.0.0.1:{port}/mcp")
    if event_store:
        logger.info("事件存储已启用 - 支持恢复")
    else:
        logger.info("事件存储已禁用 - 不支持恢复")

    # 启动服务器
    server = uvicorn.Server(config=config)
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        logger.info("服务器被用户停止")
    except Exception as e:
        logger.error(f"服务器错误：{e}")
        raise


def main():
    """主入口点。"""
    parser = argparse.ArgumentParser(description="可恢复 HTTP MCP 服务器")
    parser.add_argument("--port", type=int, default=8006, help="监听端口（默认：8006）")
    parser.add_argument("--no-event-store", action="store_true", help="禁用事件存储（无恢复支持）")
    
    args = parser.parse_args()
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 运行服务器
    asyncio.run(run_server(
        port=args.port,
        with_event_store=not args.no_event_store
    ))


if __name__ == "__main__":
    main()
