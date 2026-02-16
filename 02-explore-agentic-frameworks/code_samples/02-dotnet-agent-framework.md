# 🔍 探索 Microsoft Agent Framework - 基础代理 (.NET)

## 📋 学习目标

本示例通过 .NET 中的基础代理实现探索 Microsoft Agent Framework 的基本概念。你将学习核心的代理模式，并通过 C# 和 .NET 生态系统了解智能代理的内部工作原理。

### 你将发现什么

- 🏗️ **代理架构**：理解 .NET 中 AI 代理的基本结构
- 🛠️ **工具集成**：代理如何使用外部函数扩展能力
- 💬 **对话流程**：通过线程管理处理多轮对话和上下文
- 🔧 **配置模式**：.NET 中代理设置和管理的最佳实践

## 🎯 涵盖的关键概念

### 代理框架原则

- **自主性**：代理如何使用 .NET AI 抽象进行独立决策
- **响应性**：响应环境变化和用户输入
- **主动性**：根据目标和上下文采取主动
- **社交能力**：通过自然语言和对话线程进行交互

### 技术组件

- **AIAgent**：核心代理编排和对话管理（.NET）
- **工具函数**：使用 C# 方法和属性扩展代理能力
- **OpenAI 集成**：通过标准化的 .NET API 利用语言模型
- **安全配置**：基于环境的 API 密钥管理

## 🔧 技术栈

### 核心技术

- Microsoft Agent Framework (.NET)
- GitHub Models API 集成
- OpenAI 兼容的客户端模式
- 使用 DotNetEnv 的基于环境的配置

### 代理能力

- 自然语言理解和生成
- 函数调用和工具使用（使用 C# 属性）
- 通过对话线程进行上下文感知响应
- 具有依赖注入模式的可扩展架构

## 📚 框架比较

本示例演示了与其他代理框架相比的 Microsoft Agent Framework 方法：

| 特性 | Microsoft Agent Framework | 其他框架 |
|---------|-------------------------|------------------|
| **集成** | 原生 Microsoft 生态系统 | 兼容性各异 |
| **简洁性** | 简洁、直观的 API | 通常设置复杂 |
| **可扩展性** | 简单的工具集成 | 取决于框架 |
| **企业级准备** | 为生产环境构建 | 因框架而异 |

## 🚀 快速开始

### 前置条件

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) 或更高版本
- [GitHub Models API 访问令牌](https://docs.github.com/github-models/github-models-at-scale/using-your-own-api-keys-in-github-models)

### 所需环境变量

```bash
# zsh/bash
export GH_TOKEN=<your_github_token>
export GH_ENDPOINT=https://models.github.ai/inference
export GH_MODEL_ID=openai/gpt-5-mini
```

```powershell
# PowerShell
$env:GH_TOKEN = "<your_github_token>"
$env:GH_ENDPOINT = "https://models.github.ai/inference"
$env:GH_MODEL_ID = "openai/gpt-5-mini"
```

### 示例代码

要运行代码示例，

```bash
# zsh/bash
chmod +x ./02-dotnet-agent-framework.cs
./02-dotnet-agent-framework.cs
```

或使用 dotnet CLI：

```bash
dotnet run ./02-dotnet-agent-framework.cs
```

完整的代码请参阅 [`02-dotnet-agent-framework.cs`](./02-dotnet-agent-framework.cs)。

```csharp
#!/usr/bin/dotnet run

#:package Microsoft.Extensions.AI@10.*
#:package Microsoft.Agents.AI.OpenAI@1.*-*

using System.ClientModel;
using System.ComponentModel;

using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

using OpenAI;

// 工具函数：随机目的地生成器
// 这个静态方法将作为可调用工具供代理使用
// [Description] 属性帮助 AI 理解何时使用此函数
// 这展示了如何为 AI 代理创建自定义工具
[Description("提供一个随机的度假目的地。")]
static string GetRandomDestination()
{
    // 全球热门度假目的地列表
    // 代理将从这些选项中随机选择
    var destinations = new List<string>
    {
        "法国巴黎",
        "日本东京",
        "美国纽约",
        "澳大利亚悉尼",
        "意大利罗马",
        "西班牙巴塞罗那",
        "南非开普敦",
        "巴西里约热内卢",
        "泰国曼谷",
        "加拿大温哥华"
    };

    // 生成随机索引并返回选中的目的地
    // 使用 System.Random 进行简单随机选择
    var random = new Random();
    int index = random.Next(destinations.Count);
    return destinations[index];
}

// 从环境变量提取配置
// 获取 GitHub Models API 端点，未指定时默认为 https://models.github.ai/inference
// 获取模型 ID，未指定时默认为 openai/gpt-5-mini
// 获取 GitHub 令牌进行身份验证，未指定时抛出异常
var github_endpoint = Environment.GetEnvironmentVariable("GH_ENDPOINT") ?? "https://models.github.ai/inference";
var github_model_id = Environment.GetEnvironmentVariable("GH_MODEL_ID") ?? "openai/gpt-5-mini";
var github_token = Environment.GetEnvironmentVariable("GH_TOKEN") ?? throw new InvalidOperationException("GH_TOKEN is not set.");

// 配置 OpenAI 客户端选项
// 创建配置选项以指向 GitHub Models 端点
// 这将 OpenAI 客户端调用重定向到 GitHub 的模型推理服务
var openAIOptions = new OpenAIClientOptions()
{
    Endpoint = new Uri(github_endpoint)
};

// 使用 GitHub Models 配置初始化 OpenAI 客户端
// 使用 GitHub 令牌进行身份验证创建 OpenAI 客户端
// 配置为使用 GitHub Models 端点而非直接使用 OpenAI
var openAIClient = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions);

// 定义代理身份和详细指令
// 用于识别和日志记录的代理名称
var AGENT_NAME = "TravelAgent";

// 定义代理个性、能力和行为的详细指令
// 此系统提示塑造了代理如何响应和与用户交互
var AGENT_INSTRUCTIONS = """
你是一个有用的 AI 代理，可以帮助客户规划度假。

重要提示：当用户指定目的地时，始终为该地点进行规划。只有在用户没有指定偏好时才建议随机目的地。

对话开始时，请使用以下消息进行自我介绍：
"你好！我是你的 TravelAgent 助手。我可以帮助你规划度假并为你推荐有趣的目的地。你可以问我以下问题：
1. 为特定地点规划一日游
2. 推荐一个随机度假目的地
3. 找到具有特定特征的目的地（海滩、山脉、历史遗迹等）
4. 如果你不喜欢我的第一个建议，规划替代行程

你今天想让我帮你规划什么样的旅行？"

始终优先考虑用户偏好。如果他们提到特定目的地，如"巴厘岛"或"巴黎"，请专注于为该地点进行规划，而不是建议替代方案。
""";

// 创建具有高级旅行规划能力的 AI 代理
// 初始化完整的代理管道：OpenAI 客户端 → 聊天客户端 → AI 代理
// 配置代理的名称、详细指令和可用工具
// 这展示了带有完整配置的 .NET 代理创建模式
AIAgent agent = openAIClient
    .GetChatClient(github_model_id)
    .CreateAIAgent(
        name: AGENT_NAME,
        instructions: AGENT_INSTRUCTIONS,
        tools: [AIFunctionFactory.Create(GetRandomDestination)]
    );

// 创建新的对话线程用于上下文管理
// 初始化新的对话线程以在多次交互中维护上下文
// 线程使代理能够记住之前的交换并维护对话状态
// 这对于多轮对话和上下文理解至关重要
AgentThread thread = agent.GetNewThread();

// 执行代理：第一次旅行规划请求
// 使用可能触发随机目的地工具的初始请求运行代理
// 代理将分析请求，使用 GetRandomDestination 工具，并创建行程
// 使用 thread 参数为后续交互维护对话上下文
await foreach (var update in agent.RunStreamingAsync("帮我规划一日游", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}

Console.WriteLine();

// 执行代理：具有上下文感知的跟进请求
// 通过引用之前的响应展示上下文对话
// 代理会记住之前的目的地建议并提供替代方案
// 这展示了 .NET 代理中对话线程和上下文理解的力量
await foreach (var update in agent.RunStreamingAsync("我不喜欢那个目的地。帮我规划另一个度假。", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}
```

## 🎓 关键要点

1. **代理架构**：Microsoft Agent Framework 为在 .NET 中构建 AI 代理提供了清晰、类型安全的方法
2. **工具集成**：带有 `[Description]` 属性装饰的函数成为代理的可用水用工具
3. **对话上下文**：线程管理支持具有完整上下文感知的 多轮对话
4. **配置管理**：环境变量和安全凭证处理遵循 .NET 最佳实践
5. **OpenAI 兼容性**：GitHub Models 集成通过 OpenAI 兼容 API 无缝工作

## 🔗 额外资源

- [Microsoft Agent Framework 文档](https://learn.microsoft.com/agent-framework)
- [GitHub Models 市场](https://github.com/marketplace?type=models)
- [Microsoft.Extensions.AI](https://learn.microsoft.com/dotnet/ai/microsoft-extensions-ai)
- [.NET 单文件应用](https://devblogs.microsoft.com/dotnet/announcing-dotnet-run-app)
