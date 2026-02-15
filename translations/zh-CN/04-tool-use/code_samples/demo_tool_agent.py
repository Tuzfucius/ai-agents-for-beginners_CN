#!/usr/bin/env python3
import asyncio
import os
import sys
from datetime import datetime
from typing import Annotated

# 检查依赖项
try:
    from dotenv import load_dotenv, find_dotenv
    from openai import AsyncOpenAI
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
    from semantic_kernel.functions import kernel_function
    from semantic_kernel.contents import ChatHistory
    from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
    from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import OpenAIChatPromptExecutionSettings
except ImportError as e:
    error_message = (
        f"导入依赖项时出错：{e}\n"
        "请使用以下命令安装依赖：pip install -r requirements.txt"
    )
    raise ImportError(error_message) from e

# 加载环境变量
load_dotenv(find_dotenv())

# --- 插件 ---

class TimePlugin:
    """提供时间信息的插件。"""

    @kernel_function(description="获取当前时间和日期。")
    def get_current_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class CalculatorPlugin:
    """简单的计算器插件。"""

    @kernel_function(description="两个数字相加。")
    def add(self,
            number1: Annotated[float, "第一个数字"],
            number2: Annotated[float, "第二个数字"]) -> float:
        return number1 + number2

    @kernel_function(description="两个数字相减。")
    def subtract(self,
                 number1: Annotated[float, "第一个数字"],
                 number2: Annotated[float, "第二个数字"]) -> float:
        return number1 - number2

# --- 主 Agent 逻辑 ---

async def main():
    print("--- 演示 AI Agent（工具使用模式）---")

    # 1. 初始化 Kernel
    kernel = Kernel()

    # 2. 添加插件
    kernel.add_plugin(TimePlugin(), plugin_name="Time")
    kernel.add_plugin(CalculatorPlugin(), plugin_name="Calculator")

    # 3. 配置 AI 服务
    api_key = os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://models.inference.ai.azure.com/")
    model_id = "gpt-4o-mini" # GitHub Models 上的常用模型

    if not api_key:
        print("\n[警告] 未找到 API 密钥（GITHUB_TOKEN 或 OPENAI_API_KEY）。")
        print("此 Agent 需要 LLM 才能运行。")
        print("你可以从 https://github.com/marketplace/models 获取免费令牌")
        print("\n退出演示设置...")
        return

    print(f"使用模型初始化服务：{model_id}")

    # 初始化 Azure OpenAI 客户端（与 GitHub Models 兼容）
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=endpoint,
    )

    service = OpenAIChatCompletion(
        ai_model_id=model_id,
        async_client=client,
    )
    kernel.add_service(service)

    # 4. 创建聊天历史和设置
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "你是一个有用的助手。你可以访问时钟和计算器。"
        "必要时使用它们。"
    )

    # 启用自动函数调用
    execution_settings = OpenAIChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("\nAgent 已就绪！（输入 'exit' 退出）")
    print("试试问：'现在几点了？' 或 '55 加上 12 等于多少？'")

    # 5. 聊天循环
    while True:
        try:
            user_input = input("\n用户：")
        except EOFError:
            break

        if not user_input or user_input.lower() in ["exit", "quit"]:
            break

        chat_history.add_user_message(user_input)

        try:
            # 从 Agent 获取响应
            response = await service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Agent：{response.content}")
            chat_history.add_message(response)

        except Exception as e:
            print(f"发生错误：{e}")

if __name__ == "__main__":
    asyncio.run(main())
