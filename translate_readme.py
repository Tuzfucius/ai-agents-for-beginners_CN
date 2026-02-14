#!/usr/bin/env python3
"""翻译 README.md 文件"""

import os

README_CN = '''# AI Agents for Beginners - 中文教程

![AI Agents for Beginners](./images/repo-thumbnailv2.png)

## 构建 AI Agent 入门课程

[![GitHub license](https://img.shields.io/github/license/microsoft/ai-agents-for-beginners.svg)](https://github.com/microsoft/ai-agents-for-beginners/blob/master/LICENSE?WT.mc_id=academic-105485-koreyst)
[![GitHub contributors](https://img.shields.io/github/contributors/microsoft/ai-agents-for-beginners.svg)](https://GitHub.com/microsoft/ai-agents-for-beginners/graphs/contributors/?WT.mc_id=academic-105485-koreyst)
[![GitHub issues](https://img.shields.io/github/issues/microsoft/ai-agents-for-beginners.svg)](https://GitHub.com/microsoft/ai-agents-for-beginners/issues/?WT.mc_id=academic-105485-koreyst)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/microsoft/ai-agents-for-beginners.svg)](https://GitHub.com/microsoft/ai-agents-for-beginners/pulls/?WT.mc_id=academic-105485-koreyst)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com?WT.mc_id=academic-105485-koreyst)

### 🌐 多语言支持

#### 通过 GitHub Action 支持（自动化且始终保持最新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](./translations/ar/README.md) | [Bengali](./translations/bn/README.md) | [Bulgarian](./translations/bg/README.md) | [Burmese (Myanmar)](./translations/my/README.md) | [Chinese (Simplified)](./translations/zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](./translations/zh-HK/README.md) | [Chinese (Traditional, Macau)](./translations/zh-MO/README.md) | [Chinese (Traditional, Taiwan)](./translations/zh-TW/README.md) | [Croatian](./translations/hr/README.md) | [Czech](./translations/cs/README.md) | [Danish](./translations/da/README.md) | [Dutch](./translations/nl/README.md) | [Estonian](./translations/et/README.md) | [Finnish](./translations/fi/README.md) | [French](./translations/fr/README.md) | [German](./translations/de/README.md) | [Greek](./translations/el/README.md) | [Hebrew](./translations/he/README.md) | [Hindi](./translations/hi/README.md) | [Hungarian](./translations/hu/README.md) | [Indonesian](./translations/id/README.md) | [Italian](./translations/it/README.md) | [Japanese](./translations/ja/README.md) | [Kannada](./translations/kn/README.md) | [Korean](./translations/ko/README.md) | [Lithuanian](./translations/lt/README.md) | [Malay](./translations/ms/README.md) | [Malayalam](./translations/ml/README.md) | [Marathi](./translations/mr/README.md) | [Nepali](./translations/ne/README.md) | [Nigerian Pidgin](./translations/pcm/README.md) | [Norwegian](./translations/no/README.md) | [Persian (Farsi)](./translations/fa/README.md) | [Polish](./translations/pl/README.md) | [Portuguese (Brazil)](./translations/pt-BR/README.md) | [Portuguese (Portugal)](./translations/pt-PT/README.md) | [Punjabi (Gurmukhi)](./translations/pa/README.md) | [Romanian](./translations/ro/README.md) | [Russian](./translations/ru/README.md) | [Serbian (Cyrillic)](./translations/sr/README.md) | [Slovak](./translations/sk/README.md) | [Slovenian](./translations/sl/README.md) | [Spanish](./translations/es/README.md) | [Swahili](./translations/sw/README.md) | [Swedish](./translations/sv/README.md) | [Tagalog (Filipino)](./translations/tl/README.md) | [Tamil](./translations/ta/README.md) | [Telugu](./translations/te/README.md) | [Thai](./translations/th/README.md) | [Turkish](./translations/tr/README.md) | [Ukrainian](./translations/uk/README.md) | [Urdu](./translations/ur/README.md) | [Vietnamese](./translations/vi/README.md)

> **prefer本地克隆？**

> 该仓库包含50多种语言翻译，这会显著增加下载大小。若要在不包含翻译的情况下克隆，请使用稀疏检出：
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft/ai-agents-for-beginners.git
> cd ai-agents-for-beginners
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
> 这样可以获取完成课程所需的所有内容，下载速度更快。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

**如果需要其他翻译语言支持，请查看[这里](https://github.com/Azure/co-op-translator/blob/main/getting_started/supported-languages.md)**

[![GitHub watchers](https://img.shields.io/github/watchers/microsoft/ai-agents-for-beginners.svg?style=social&label=Watch)](https://GitHub.com/microsoft/ai-agents-for-beginners/watchers/?WT.mc_id=academic-105485-koreyst)
[![GitHub forks](https://img.shields.io/github/forks/microsoft/ai-agents-for-beginners.svg?style=social&label=Fork)](https://GitHub.com/microsoft/ai-agents-for-beginners/network/?WT.mc_id=academic-105485-koreyst)
[![GitHub stars](https://img.shields.io/github/stars/microsoft/ai-agents-for-beginners.svg?style=social&label=Star)](https://GitHub.com/microsoft/ai-agents-for-beginners/stargazers/?WT.mc_id=academic-105485-koreyst)

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/nTYy5BXMWG)


## 🌱 开始学习

本课程包含构建 AI Agent 基础知识的各个章节。每个章节涵盖独立的主题，可以从任意章节开始学习！

本课程支持多语言。请查看[可用语言列表](#-多语言支持)。

如果这是您第一次使用生成式 AI 模型构建应用，请查看我们的[生成式 AI 入门](https://aka.ms/genai-beginners)课程，其中包含 21 节关于 GenAI 构建的课程。

别忘了[给本仓库加星标 (🌟)](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars?WT.mc_id=academic-105485-koreyst)和[fork 本仓库](https://github.com/microsoft/ai-agents-for-beginners/fork)来运行代码。

### 认识其他学习者，解决你的问题

如果您在构建 AI Agent 时遇到任何问题或有任何疑问，请加入 [Microsoft Foundry Discord](https://aka.ms/ai-agents/discord) 中的专属 Discord 频道。

### 课程要求

本课程的每个章节都包含代码示例，位于 code_samples 文件夹中。您可以[fork 本仓库](https://github.com/microsoft/ai-agents-for-beginners/fork)创建自己的副本。

本课程的代码示例使用 Azure AI Foundry 和 GitHub Model Catalogs 来与大语言模型交互：

- [GitHub Models](https://aka.ms/ai-agents-beginners/github-models) - 免费/有限
- [Azure AI Foundry](https://aka.ms/ai-agents-beginners/ai-foundry) - 需要 Azure 账户

本课程还使用 Microsoft 的以下 AI Agent 框架和服务：

- [Microsoft Agent Framework (MAF) - 新增！](https://aka.ms/ai-agents-beginners/agent-framewrok)
- [Azure AI Agent Service](https://aka.ms/ai-agents-beginners/ai-agent-service)
- [Semantic Kernel](https://aka.ms/ai-agents-beginners/semantic-kernel)
- [AutoGen](https://aka.ms/ai-agents/autogen)

有关运行本课程代码的更多信息，请转到[课程设置](./00-course-setup/README.md)。

## 🙏 想要帮助我们？

您有任何建议或发现拼写或代码错误？请[提交 issue](https://github.com/microsoft/ai-agents-for-beginners/issues?WT.mc_id=academic-105485-koreyst)或[创建 pull request](https://github.com/microsoft/ai-agents-for-beginners/pulls?WT.mc_id=academic-105485-koreyst)。



## 📂 每个章节包括

- 位于 README 中的文字课程和简短视频
- 支持 Azure AI Foundry 和 GitHub Models（免费）的 Python 代码示例
- 继续学习的额外资源链接


## 🗃️ 课程目录

| **课程**                                   | **文字与代码**                                    | **视频**                                                  | **额外学习**                                                                     |
|----------------------------------------------|----------------------------------------------------|------------------------------------------------------------|----------------------------------------------------------------------------------------|
| AI Agent 入门与使用案例                       | [链接](./01-intro-to-ai-agents/README.md)          | [视频](https://youtu.be/3zgm60bXmQk?si=z8QygFvYQv-9WtO1)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 探索 AI Agent 框架                           | [链接](./02-explore-agentic-frameworks/README.md)  | [视频](https://youtu.be/ODwF-EZo_O8?si=Vawth4hzVaHv-u0H)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 理解 AI Agent 设计模式                       | [链接](./03-agentic-design-patterns/README.md)     | [视频](https://youtu.be/m9lM8qqoOEA?si=BIzHwzstTPL8o9GF)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 工具使用设计模式                             | [链接](./04-tool-use/README.md)                    | [视频](https://youtu.be/vieRiPRx-gI?si=2z6O2Xu2cu_Jz46N)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| Agentic RAG                                  | [链接](./05-agentic-rag/README.md)                 | [视频](https://youtu.be/WcjAARvdL7I?si=gKPWsQpKiIlDH9A3)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 构建可信赖的 AI Agent                        | [链接](./06-building-trustworthy-agents/README.md) | [视频](https://youtu.be/iZKkMEGBCUQ?si=jZjpiMnGFOE9L8OK ) | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 规划设计模式                                 | [链接](./07-planning-design/README.md)             | [视频](https://youtu.be/kPfJ2BrBCMY?si=6SC_iv_E5-mzucnC)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 多 Agent 设计模式                             | [链接](./08-multi-agent/README.md)                 | [视频](https://youtu.be/V6HpE9hZEx0?si=rMgDhEu7wXo2uo6g)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 元认知设计模式                               | [链接](./09-metacognition/README.md)               | [视频](https://youtu.be/His9R6gw6Ec?si=8gck6vvdSNCt6OcF)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 生产环境中的 AI Agent                        | [链接](./10-ai-agents-production/README.md)        | [视频](https://youtu.be/l4TP6IyJxmQ?si=31dnhexRo6yLRJDl)  | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 使用 Agentic 协议 (MCP, A2A 和 NLWeb)         | [链接](./11-agentic-protocols/README.md)           | [视频](https://youtu.be/X-Dh9R3Opn8)                                 | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| AI Agent 的上下文工程                         | [链接](./12-context-engineering/README.md)         | [视频](https://youtu.be/F5zqRV7gEag)                                 | [链接](https://aka.ms/ai-agents-beginners/collection?WT.mc_id=academic-105485-koreyst) |
| 管理 Agent 记忆                             | [链接](./13-agent-memory/README.md)     |      [视频](https://youtu.be/QrYbHesIxpw?si=vZkVwKrQ4ieCcIPx)                                                      |                                                                                        |
| 探索 Microsoft Agent 框架                     | [链接](./14-microsoft-agent-framework/README.md)                            |                                                            |                                                                                        |
| 构建计算机使用 Agent (CUA)                    | 即将推出                            |                                                            |                                                                                        |
| 部署可扩展的 Agent                           | 即将推出                            |                                                            |                                                                                        |
| 创建本地 AI Agent                            | 即将推出                               |                                                            |                                                                                        |
| 保护 AI Agent                                | 即将推出                               |                                                            |                                                                                        |

## 🎒 其他课程

我们团队还制作了其他课程！请查看：

<!-- CO-OP TRANSLATOR OTHER COURSES START -->
### LangChain
[![LangChain4j for Beginners](https://img.shields.io/badge/LangChain4j%20for%20Beginners-22C55E?style=for-the-badge&&labelColor=E5E7EB&color=0553D6)](https://aka.ms/langchain4j-for-beginners)
[![LangChain.js for Beginners](https://img.shields.io/badge/LangChain.js%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=0553D6)](https://aka.ms/langchainjs-for-beginners?WT.mc_id=m365-94501-dwahlin)
[![LangChain for Beginners](https://img.shields.io/badge/LangChain%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=0553D6)](https://github.com/microsoft/langchain-for-beginners?WT.mc_id=m365-94501-dwahlin)
---

### Azure / Edge / MCP / Agents
[![AZD for Beginners](https://img.shields.io/badge/AZD%20for%20Beginners-0078D4?style=for-the-badge&labelColor=E5E7EB&color=0078D4)](https://github.com/microsoft/AZD-for-beginners?WT.mc_id=academic-105485-koreyst)
[![Edge AI for Beginners](https://img.shields.io/badge/Edge%20AI%20for%20Beginners-00B8E4?style=for-the-badge&labelColor=E5E7EB&color=00B8E4)](https://github.com/microsoft/edgeai-for-beginners?WT.mc_id=academic-105485-koreyst)
[![MCP for Beginners](https://img.shields.io/badge/MCP%20for%20Beginners-009688?style=for-the-badge&labelColor=E5E7EB&color=009688)](https://github.com/microsoft/mcp-for-beginners?WT.mc_id=academic-105485-koreyst)
[![AI Agents for Beginners](https://img.shields.io/badge/AI%20Agents%20for%20Beginners-00C49A?style=for-the-badge&labelColor=E5E7EB&color=00C49A)](https://github.com/microsoft/ai-agents-for-beginners?WT.mc_id=academic-105485-koreyst)

---
 
### 生成式 AI 系列
[![生成式 AI 入门](https://img.shields.io/badge/Generative%20AI%20for%20Beginners-8B5CF6?style=for-the-badge&labelColor=E5E7EB&color=8B5CF6)](https://github.com/microsoft/generative-ai-for-beginners?WT.mc_id=academic-105485-koreyst)
[![生成式 AI (.NET)](https://img.shields.io/badge/Generative%20AI%20(.NET)-9333EA?style=for-the-badge&labelColor=E5E7EB&color=9333EA)](https://github.com/microsoft/Generative-AI-for-beginners-dotnet?WT.mc_id=academic-105485-koreyst)
[![生成式 AI (Java)](https://img.shields.io/badge/Generative%20AI%20(Java)-C084FC?style=for-the-badge&labelColor=E5E7EB&color=C084FC)](https://github.com/microsoft/generative-ai-for-beginners-java?WT.mc_id=academic-105485-koreyst)
[![生成式 AI (JavaScript)](https://img.shields.io/badge/Generative%20AI%20(JavaScript)-E879F9?style=for-the-badge&labelColor=E5E7EB&color=E879F9)](https://github.com/microsoft/generative-ai-with-javascript?WT.mc_id=academic-105485-koreyst)

---
 
### 核心学习
[![机器学习入门](https://img.shields.io/badge/ML%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=22C55E)](https://aka.ms/ml-beginners?WT.mc_id=academic-105485-koreyst)
[![数据科学入门](https://img.shields.io/badge/Data%20Science%20for%20Beginners-84CC16?style=for-the-badge&labelColor=E5E7EB&color=84CC16)](https://aka.ms/datascience-beginners?WT.mc_id=academic-105485-koreyst)
[![AI 入门](https://img.shields.io/badge/AI%20for%20Beginners-A3E635?style=for-the-badge&labelColor=E5E7EB&color=A3E635)](https://aka.ms/ai-beginners?WT.mc_id=academic-105485-koreyst)
[![网络安全入门](https://img.shields.io/badge/Cybersecurity%20for%20Beginners-F97316?style=for-the-badge&labelColor=E5E7EB&color=F97316)](https://github.com/microsoft/Security-101?WT.mc_id=academic-96948-sayoung)
[![Web 开发入门](https://img.shields.io/badge/Web%20Dev%20for%20Beginners-EC4899?style=for-the-badge&labelColor=E5E7EB&color=EC4899)](https://aka.ms/webdev-beginners?WT.mc_id=academic-105485-koreyst)
[![物联网入门](https://img.shields.io/badge/IoT%20for%20Beginners-14B8A6?style=for-the-badge&labelColor=E5E7EB&color=14B8A6)](https://aka.ms/iot-beginners?WT.mc_id=academic-105485-koreyst)
[![XR 开发入门](https://img.shields.io/badge/XR%20Development%20for%20Beginners-38BDF8?style=for-the-badge&labelColor=E5E7EB&color=38BDF8)](https://github.com/microsoft/xr-development-for-beginners?WT.mc_id=academic-105485-koreyst)

---
 
### Copilot 系列
[![AI 配对编程的 Copilot](https://img.shields.io/badge/Copilot%20for%20AI%20Paired%20Programming-FACC15?style=for-the-badge&labelColor=E5E7EB&color=FACC15)](https://aka.ms/GitHubCopilotAI?WT.mc_id=academic-105485-koreyst)
[![C#/.NET 的 Copilot](https://img.shields.io/badge/Copilot%20for%20C%23/.NET-FBBF24?style=for-the-badge&labelColor=E5E7EB&color=FBBF24)](https://github.com/microsoft/mastering-github-copilot-for-dotnet-csharp-developers?WT.mc_id=academic-105485-koreyst)
[![Copilot 冒险](https://img.shields.io/badge/Copilot%20Adventure-FDE68A?style=for-the-badge&labelColor=E5E7EB&color=FDE68A)](https://github.com/microsoft/CopilotAdventures?WT.mc_id=academic-105485-koreyst)
<!-- CO-OP TRANSLATOR OTHER COURSES END -->

## 🌟 社区感谢

感谢 [Shivam Goyal](https://www.linkedin.com/in/shivam2003/) 贡献了展示 Agentic RAG 的重要代码示例。

## 贡献

本项目欢迎贡献和建议。大多数贡献需要您同意贡献者许可协议 (CLA)，声明您有权并且确实授予我们使用您贡献的权利。有关详细信息，请访问 <https://cla.opensource.microsoft.com>。

当您提交 pull request 时，CLA 机器人将自动确定您是否需要提供 CLA 并适当地装饰 PR（例如，状态检查、评论）。只需按照机器人提供的说明操作即可。在使用我们的 CLA 的所有仓库中，您只需要这样做一次。

本项目采用了 [Microsoft 开源行为准则](https://opensource.microsoft.com/codeofconduct/)。有关更多信息，请参阅[行为准则常见问题](https://opensource.microsoft.com/codeofconduct/faq/)或联系 [opencode@microsoft.com](mailto:opencode@microsoft.com) 提出任何其他问题或评论。

## 商标

本项目可能包含项目、产品或服务的商标或徽标。Microsoft 商标或徽标的授权使用必须遵守 [Microsoft 商标和品牌指南](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general)。在本项目的修改版本中使用 Microsoft 商标或徽标不得造成混淆或暗示 Microsoft 赞助。任何第三方商标或徽标的使用均须遵守这些第三方的政策。

## 获取帮助

如果您在构建 AI 应用时遇到任何问题或有任何疑问，请加入：

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/nTYy5BXMWG)

如果您在构建过程中有产品反馈或错误，请访问：

[![Microsoft Foundry 开发者论坛](https://img.shields.io/badge/GitHub-Microsoft_Foundry_Developer_Forum-blue?style=for-the-badge&logo=github&color=000000&logoColor=fff)](https://aka.ms/foundry/forum)
'''

# 保存翻译文件
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(README_CN)

print("✅ 已翻译 README.md")
