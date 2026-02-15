#!/usr/bin/dotnet run

#:package Microsoft.Extensions.AI@10.1.1
#:package Microsoft.Extensions.AI.OpenAI@10.1.1-preview.1.25612.2
#:package Microsoft.Agents.AI.OpenAI@1.0.0-preview.251219.1

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

// 创建具有旅行规划功能的 AI Agent
// 初始化完整的 Agent 管道：OpenAI 客户端 → 聊天客户端 → AI Agent
// 配置 Agent 的名称、指令和可用工具
// Agent 现在可以使用 GetRandomDestination 函数规划旅行
AIAgent agent = openAIClient
    .GetChatClient(github_model_id)
    .AsIChatClient()
    .CreateAIAgent(
        instructions: "你是一个有用的 AI Agent，可以帮助客户规划随机目的地的度假行程",
        tools: [AIFunctionFactory.Create(GetRandomDestination)]
    );

// 执行 Agent：规划一日游
// 启用流式运行 Agent 以实时显示响应
// 显示 Agent 在生成内容时的思考和响应
// 通过即时反馈提供更好的用户体验
await foreach (var update in agent.RunStreamingAsync("帮我规划一日游"))
{
    await Task.Delay(10);
    Console.Write(update);
}
