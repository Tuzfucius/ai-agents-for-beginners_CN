#!/usr/bin/env python3
"""批量翻译章节 README"""

import os
import subprocess

# 要翻译的章节
CHAPTERS = [
    "00-course-setup",
    "01-intro-to-ai-agents", 
    "02-explore-agentic-frameworks",
    "03-agentic-design-patterns",
    "04-tool-use",
    "05-agentic-rag",
    "06-building-trustworthy-agents",
    "07-planning-design",
    "08-multi-agent",
    "09-metacognition",
    "10-ai-agents-production",
    "11-agentic-protocols",
    "12-context-engineering",
    "13-agent-memory",
    "14-microsoft-agent-framework",
]

def translate_file(input_path, output_path):
    """使用简单的中文字符替换进行初步翻译"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经是中文
    chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
    if chinese_chars > len(content) * 0.3:
        print(f"  ⏭️  跳过（已包含中文）")
        return
    
    # 简单翻译一些关键词
    replacements = {
        "Introduction to AI Agents": "AI Agent 入门",
        "Exploring Agentic Frameworks": "探索 Agentic 框架",
        "Understanding AI Agentic Design Patterns": "理解 Agentic 设计模式",
        "Tool Use": "工具使用",
        "Agentic RAG": "Agentic RAG",
        "Building Trustworthy Agents": "构建可信赖的 Agent",
        "Planning Design": "规划设计",
        "Multi-Agent": "多 Agent 系统",
        "Metacognition": "元认知",
        "AI Agents in Production": "生产环境中的 AI Agent",
        "Using Agentic Protocols": "使用 Agentic 协议",
        "Context Engineering": "上下文工程",
        "Managing Agentic Memory": "管理 Agent 记忆",
        "Exploring Microsoft Agent Framework": "探索 Microsoft Agent 框架",
        "Building Computer Use Agents": "构建计算机使用 Agent",
        "Course Setup": "课程设置",
        
        # 关键词翻译
        "Introduction": "简介",
        "Learning Goals": "学习目标",
        "## Learning Goals": "## 学习目标",
        "## Introduction": "## 简介",
        "## What": "## 什么是",
        "Sample Code": "示例代码",
        "Previous Lesson": "上一课",
        "Next Lesson": "下一课",
        "This lesson covers": "本节课涵盖",
        "After completing this lesson": "完成本节课后",
        
        # 常见词汇
        "agent": "Agent",
        "Agent": "Agent",
        "agents": "Agent",
        "Agents": "Agent",
        "LLM": "大型语言模型",
        "framework": "框架",
        "Framework": "框架",
        "pattern": "模式",
        "Pattern": "模式",
        "tool": "工具",
        "Tool": "工具",
        "memory": "记忆",
        "Memory": "记忆",
    }
    
    for eng, cn in replacements.items():
        content = content.replace(eng, cn)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ 已处理")

# 主流程
print("=== 翻译章节 README 文件 ===\n")

for chapter in CHAPTERS:
    readme_path = f"{chapter}/README.md"
    if os.path.exists(readme_path):
        print(f"📄 {chapter}")
        translate_file(readme_path, readme_path)
    else:
        print(f"⚠️  {chapter}: README.md 不存在")

print("\n=== 完成 ===")
