#!/usr/bin/dotnet run

#:package Microsoft.Extensions.AI@10.*
#:package Microsoft.Extensions.AI.OpenAI@10.*-*
#:package Microsoft.Agents.AI.OpenAI@1.*-*

using System.ClientModel;
using System.ComponentModel;

using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

using OpenAI;

// 工具函数：随机目的地生成器
// 这个静态方法将作为可调用工具提供给 Agent
// [Description] 属性帮助 AI 理解何时使用此函数
// 这展示了如何为 AI Agent 创建自定义工具
[Description("提供一个随机的度假目的地。")]
static string GetRandomDestination()
{
    // 全球热门度假目的地列表
    // Agent 将从这些选项中随机选择
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

    // 生成随机索引并返回选择的目的地
    // 使用 System.Random 进行简单随机选择
    var random = new Random();
    int index = random.Next(destinations.Count);
    return destinations[index];
}

// 从环境变量中提取配置
// 获取 GitHub Models API 端点，未指定时默认为 https://models.github.ai/inference
// 获取模型 ID，未指定时默认为 openai/gpt-5-mini
// 获取 GitHub 认证令牌，未指定时抛出异常
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
// 配置它使用 GitHub Models 端点而不是直接使用 OpenAI
var openAIClient = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions);

// 定义 Agent 身份和详细指令
// 用于标识和日志记录的 Agent 名称
var AGENT_NAME = "TravelAgent";

// 定义 Agent 个性、能力和行为的详细指令
// 这个系统提示塑造了 Agent 如何响应和与用户交互
var AGENT_INSTRUCTIONS = """
你是一个有用的 AI Agent，可以帮助客户规划度假行程。

重要提示：当用户指定目的地时，始终为该地点进行规划。只有在用户未指定偏好时才建议随机目的地。

对话开始时，用以下消息介绍自己：
"你好！我是你的 TravelAgent 助手。我可以帮助你规划度假并为你推荐有趣的目的地。你可以问我以下问题：
1. 为特定地点规划一日游
2. 推荐随机度假目的地
3. 寻找具有特定特征的目的地（海滩、山脉、历史遗迹等）
4. 如果你不喜欢我的第一个建议，规划替代行程

今天你想让我帮你规划什么样的行程？"

始终优先考虑用户偏好。如果他们提到特定目的地，如"巴厘岛"或"巴黎"，请专注于为该地点进行规划，而不是建议替代方案。
""";

// 创建具有高级旅行规划功能的 AI Agent
// 初始化完整的 Agent 管道：OpenAI 客户端 → 聊天客户端 → AI Agent
// 使用名称、详细指令和可用工具配置 Agent
// 这展示了 .NET Agent 创建模式及完整配置
AIAgent agent = openAIClient
    .GetChatClient(github_model_id)
    .AsIChatClient()
    .CreateAIAgent(
        name: AGENT_NAME,
        instructions: AGENT_INSTRUCTIONS,
        tools: [AIFunctionFactory.Create(GetRandomDestination)]
    );

// 创建新对话线程以进行上下文管理
// 初始化新对话线程以在多次交互中维护上下文
// 线程使 Agent 能够记住之前的对话并维护对话状态
// 这对于多轮对话和上下文理解至关重要
AgentThread thread = agent.GetNewThread();

// 执行 Agent：第一个旅行规划请求
// 使用可能会触发随机目的地工具的初始请求运行 Agent
// Agent 将分析请求，使用 GetRandomDestination 工具，并创建行程
// 使用线程参数维护后续交互的对话上下文
await foreach (var update in agent.RunStreamingAsync("帮我规划一日游", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}

Console.WriteLine();

// 执行 Agent：具有上下文感知的跟进请求
// 通过引用之前的响应展示上下文对话
// Agent 会记住之前的目的地建议并提供替代方案
// 这展示了 .NET Agent 中对话线程和上下文理解的力量
await foreach (var update in agent.RunStreamingAsync("我不喜欢那个目的地。帮我规划另一个度假行程。", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}
