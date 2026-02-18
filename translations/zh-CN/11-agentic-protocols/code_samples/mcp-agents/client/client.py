#!/usr/bin/env python3
"""
用于 Agent-to-Agent 通信教程的交互式 MCP 客户端
"""

import asyncio
import argparse
import logging
from typing import Dict, Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.server.streamable_http import MCP_SESSION_ID_HEADER, MCP_PROTOCOL_VERSION_HEADER
from mcp.shared.message import ClientMessageMetadata
import mcp.types as types
from rich.console import Console
from rich.panel import Panel

from .utils import TokenManager, cast_input_value

console = Console()


def display_tools(tools):
    """将可用工具显示为简单列表。"""
    console.print("[bold]可用工具：[/bold]")
    for tool in tools:
        tool_type = "🤖" if any(word in tool.name.lower() for word in ["agent", "travel", "research"]) else "🔧"
        console.print(f"  {tool_type} [cyan]{tool.name}[/cyan]")
    console.print()
    console.print("[dim]输入工具名称以使用默认参数运行它[/dim]")


def extract_text_content(result) -> str:
    """从工具结果中提取文本内容。"""
    for content in result.content:
        if hasattr(content, 'text'):
            return content.text
    return "没有可用的文本内容"


async def execute_tool_with_resumption(session, command: str, args: dict, get_session_id, on_resumption_token_update, existing_tokens=None, token_manager=None):
    """使用 send_request 执行具有恢复支持的工具。"""
    current_session_id = get_session_id()
    if not current_session_id:
        raise RuntimeError("没有可用的会话 ID - 恢复需要有效的会话")
    
    session_id = current_session_id
    
    # 如果我们有现有的恢复令牌，将其传递以进行恢复
    if existing_tokens and existing_tokens.get("resumption_token"):
        metadata = ClientMessageMetadata(
            resumption_token=existing_tokens["resumption_token"],
        )
    else:
        # 创建增强的回调，在收到令牌时立即保存工具上下文
        def enhanced_callback(token: str):
            # 由于回调会立即使用实际的恢复令牌触发，
            # 立即保存恢复所需的所有内容
            protocol_version = getattr(session, 'protocol_version', None)
            if token_manager:
                token_manager.save_tokens(session_id, token, protocol_version, command, args)
            # 同时调用原始回调
            return on_resumption_token_update(session_id, token, command, args)
        
        metadata = ClientMessageMetadata(
            on_resumption_token_update=enhanced_callback,
        )
    
    result = await session.send_request(
        types.ClientRequest(
            types.CallToolRequest(
                method="tools/call",
                params=types.CallToolRequestParams(
                    name=command,
                    arguments=args
                ),
            )
        ),
        types.CallToolResult,
        metadata=metadata,
    )
    
    return result


async def interactive_mode(server_url: str):
    """运行带有工具探索的交互模式。"""
    # 配置日志以抑制嘈杂的 SSE 解析错误
    logging.getLogger('mcp.client.streamable_http').setLevel(logging.ERROR)
    
    # 过滤特定的 SSE JSON 解析错误
    class SSEFilter(logging.Filter):
        def filter(self, record):
            # 抑制 "Error parsing SSE message" 和 JSON 验证错误
            if ("Error parsing SSE message" in record.getMessage() or 
                "ValidationError" in record.getMessage() or
                "EOF while parsing" in record.getMessage()):
                return False
            return True
