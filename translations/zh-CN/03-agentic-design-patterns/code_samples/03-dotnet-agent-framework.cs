#!/usr/bin/dotnet run

#:package Microsoft.Extensions.AI@10.*
#:package Microsoft.Extensions.AI.OpenAI@10.*-*
#:package Microsoft.Agents.AI.OpenAI@1.*-*

using System.ClientModel;
using System.ComponentModel;

using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

using OpenAI;

// ============================================================================
// AGENTIC DESIGN PRINCIPLES DEMONSTRATION
// ============================================================================
// This sample demonstrates the three key design principles from the lesson:
// 1. TRANSPARENCY: The agent explains what it's doing and why
// 2. CONTROL: Users can customize preferences and the agent respects them
// 3. CONSISTENCY: The agent uses a predictable, standardized interaction pattern
// ============================================================================

// 工具函数：随机目的地生成器
// 透明性：清晰的描述帮助用户理解此工具的用途
[Description("提供一个随机的度假目的地。返回城市和国家。")]
static string GetRandomDestination()
{
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

    var random = new Random();
    int index = random.Next(destinations.Count);
    return destinations[index];
}

// 工具函数：用户偏好存储（展示 CONTROL 原则）
// 控制权：此工具允许用户设置和管理他们的偏好
[Description("保存用户行程规划的偏好。当用户指定偏好时使用，如预算等级（budget/moderate/luxury）、旅行风格（adventure/relaxation/cultural）或时长偏好。")]
static string SaveUserPreference(
    [Description("正在保存的偏好类型，例如 'budget'、'style'、'duration'")] string preferenceType,
    [Description("偏好的值")] string preferenceValue)
{
    // 在实际应用中，这会持久化到数据库
    Console.WriteLine($"\n[透明度] 保存偏好: {preferenceType} = {preferenceValue}");
    return $"偏好已保存：{preferenceType} 现在设置为 '{preferenceValue}'。我会在未来的建议中记住这一点。";
}

// 从环境变量中提取配置
var github_endpoint = Environment.GetEnvironmentVariable("GH_ENDPOINT") ?? "https://models.github.ai/inference";
var github_model_id = Environment.GetEnvironmentVariable("GH_MODEL_ID") ?? "openai/gpt-5-mini";
var github_token = Environment.GetEnvironmentVariable("GH_TOKEN") ?? throw new InvalidOperationException("GH_TOKEN is not set.");

// 配置 OpenAI 客户端选项
var openAIOptions = new OpenAIClientOptions()
{
    Endpoint = new Uri(github_endpoint)
};

var openAIClient = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions);

// Agent 身份
var AGENT_NAME = "TravelAgent";

// ============================================================================
// AGENT INSTRUCTIONS - 展示设计原则
// ============================================================================
// 这些指令将三个设计原则直接嵌入到 Agent 的行为中
var AGENT_INSTRUCTIONS = """
你是一个展示 Agentic 设计原则的有用 AI Agent。

## 你的核心原则

**透明度**：始终解释你在做什么以及为什么。
- 使用工具时，简短解释你调用的工具以及原因
- 与用户分享你的推理过程
- 对局限性或不确定性保持诚实

**控制权**：尊重用户偏好并允许自定义。
- 在做假设之前询问偏好
- 使用 SaveUserPreference 工具记住用户的选择
- 始终优先考虑明确的用户请求而非默认值

**一致性**：使用可预测的标准化交互模式。
- 每次对话以友好的问候开始
- 以清晰、有组织的格式组织回复
- 对类似操作使用相似的措辞

## 初始问候（一致性）

对话开始时，始终用以下消息介绍自己：
"你好！我是 TravelAgent，你的 AI 度假规划助手。

🔍 **透明度**：我会始终解释我的推理和我使用的工具。
🎮 **控制权**：告诉我你的偏好，我会记住它们。
🔄 **一致性**：我遵循可预测的模式，让规划变得简单。

今天你想让我帮你规划什么样的行程？"

## 指南
- 当用户指定目的地时，为该地点进行规划
- 只有在用户未指定目的地时才建议随机目的地
- 在更改偏好之前始终确认
""";

// 使用设计原则创建 AI Agent
AIAgent agent = openAIClient
    .GetChatClient(github_model_id)
    .AsIChatClient()
    .CreateAIAgent(
        name: AGENT_NAME,
        instructions: AGENT_INSTRUCTIONS,
        tools: [
            AIFunctionFactory.Create(GetRandomDestination),
            AIFunctionFactory.Create(SaveUserPreference)
        ]
    );

// 创建对话线程以进行上下文管理
AgentThread thread = agent.GetNewThread();

// ============================================================================
// 演示：从 "Hello" 开始以触发问候（修复 #402）
// ============================================================================
Console.WriteLine("=== 展示 Agentic 设计原则 ===\n");
Console.WriteLine("用户：你好\n");
Console.WriteLine("Agent 回复：");

await foreach (var update in agent.RunStreamingAsync("你好", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}

Console.WriteLine("\n");

// ============================================================================
// 演示：用户设置偏好（CONTROL 原则）
// ============================================================================
Console.WriteLine("---");
Console.WriteLine("用户：我偏好豪华旅行和文化体验。\n");
Console.WriteLine("Agent 回复：");

await foreach (var update in agent.RunStreamingAsync("我偏好豪华旅行和文化体验。", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}

Console.WriteLine("\n");

// ============================================================================
// 演示：Agent 使用工具并保持透明
// ============================================================================
Console.WriteLine("---");
Console.WriteLine("用户：给我推荐一个目的地。\n");
Console.WriteLine("Agent 回复：");

await foreach (var update in agent.RunStreamingAsync("给我推荐一个目的地。", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}
