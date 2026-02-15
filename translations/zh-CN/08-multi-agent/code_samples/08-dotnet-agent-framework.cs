#!/usr/bin/dotnet run
#:package Microsoft.Extensions.AI.Abstractions@9.9.1
#:package Azure.AI.Agents.Persistent@1.2.0-beta.4
#:package Azure.Identity@1.15.0
#:package System.Linq.Async@6.0.3
#:package Microsoft.Extensions.AI@9.9.1
#:package DotNetEnv@3.1.1
#:package OpenTelemetry.Api@1.12.0
#:package Microsoft.Agents.AI.Workflows@1.0.0-preview.251001.3
#:package Microsoft.Agents.AI.OpenAI@1.0.0-preview.251001.2

using System;
using System.ClientModel;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Workflows;
using OpenAI;
using DotNetEnv;

// 加载环境变量
Env.Load("../../../.env");

// 从环境变量获取配置
var github_endpoint = Environment.GetEnvironmentVariable("GITHUB_ENDPOINT") ?? throw new InvalidOperationException("GITHUB_ENDPOINT is not set.");
var github_model_id = Environment.GetEnvironmentVariable("GITHUB_MODEL_ID") ?? "gpt-4o-mini";
var github_token = Environment.GetEnvironmentVariable("GITHUB_TOKEN") ?? throw new InvalidOperationException("GITHUB_TOKEN is not set.");

// 为 GitHub Models 配置 OpenAI 客户端
var openAIOptions = new OpenAIClientOptions()
{
    Endpoint = new Uri(github_endpoint)
};

var openAIClient = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions);

// 定义 Agent 角色和指令
const string REVIEWER_NAME = "Concierge";
const string REVIEWER_INSTRUCTIONS = @"""
    你是一位酒店礼宾员，对为旅行者提供最本地、最真实的体验有自己的看法。
    目标是确定前台旅行代理是否为旅行者推荐了最好的非旅游体验。
    如果是这样，请批准。
    如果没有，请在不使用具体示例的情况下提供如何改进建议的见解。
    """;

const string FRONTDESK_NAME = "FrontDesk";
const string FRONTDESK_INSTRUCTIONS = @"""
    你是一位有十年经验的前台旅行代理，因处理众多客户而以简洁著称。
    目标是，为旅行者提供最好的活动和地点。
    每次回复只提供一个建议。
    你对当前目标非常专注。
    不要浪费时间闲聊。
    在完善想法时考虑建议。
    """;

// 创建 Agent 选项
ChatClientAgentOptions frontdeskAgentOptions = new(name: FRONTDESK_NAME, instructions: FRONTDESK_INSTRUCTIONS);
ChatClientAgentOptions reviewerAgentOptions = new(name: REVIEWER_NAME, instructions: REVIEWER_INSTRUCTIONS);

// 创建 Agents
AIAgent reviewerAgent = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions).GetChatClient(github_model_id).CreateAIAgent(
    reviewerAgentOptions);
AIAgent frontdeskAgent = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions).GetChatClient(github_model_id).CreateAIAgent(
    frontdeskAgentOptions);

// 构建带有 Agent 协调的工作流
var workflow = new WorkflowBuilder(frontdeskAgent)
            .AddEdge(frontdeskAgent, reviewerAgent)
            .Build();

// 使用流式执行工作流
StreamingRun run = await InProcessExecution.StreamAsync(workflow, new ChatMessage(ChatRole.User, "我想去巴黎。"));

await run.TrySendMessageAsync(new TurnToken(emitEvents: true));

string strResult = "";

// 处理流式事件
await foreach (WorkflowEvent evt in run.WatchStreamAsync().ConfigureAwait(false))
{
    if (evt is AgentRunUpdateEvent executorComplete)
    {
        strResult += executorComplete.Data;
        Console.WriteLine($"{executorComplete.ExecutorId}: {executorComplete.Data}");
    }
}

// 显示最终结果
Console.WriteLine("\n最终结果：");
Console.WriteLine(strResult);
