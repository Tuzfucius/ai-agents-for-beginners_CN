#!/usr/bin/dotnet run
#:package Microsoft.Extensions.AI@9.9.1
#:package Microsoft.Agents.AI.OpenAI@1.0.0-preview.251001.3
#:package Microsoft.Agents.AI@1.0.0-preview.251001.3
#:package DotNetEnv@3.1.1

using System;
using System.ClientModel;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI;
using OpenAI;
using DotNetEnv;

// 从 .env 文件加载环境变量
Env.Load("../../../.env");

// 获取环境配置
var github_endpoint = Environment.GetEnvironmentVariable("GITHUB_ENDPOINT") ?? throw new InvalidOperationException("GITHUB_ENDPOINT is not set.");
var github_model_id = Environment.GetEnvironmentVariable("GITHUB_MODEL_ID") ?? "gpt-4o-mini";
var github_token = Environment.GetEnvironmentVariable("GITHUB_TOKEN") ?? throw new InvalidOperationException("GITHUB_TOKEN is not set.");

// 配置 OpenAI 客户端选项
var openAIOptions = new OpenAIClientOptions()
{
    Endpoint = new Uri(github_endpoint)
};

// 创建 OpenAI 客户端
var openAIClient = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions);

// 定义 Agent 配置
const string AGENT_NAME = "TravelPlanAgent";

const string AGENT_INSTRUCTIONS = @"你是一个规划 Agent。
    你的工作是根据用户的请求决定运行哪些 Agent。
    以下是专门处理不同任务的可用 Agent：
    - FlightBooking：用于预订航班和提供航班信息
    - HotelBooking：用于预订酒店和提供酒店信息
    - CarRental：用于预订车辆和提供租车信息
    - ActivitiesBooking：用于预订活动和提供活动信息
    - DestinationInfo：用于提供目的地信息
    - DefaultAgent：用于处理一般请求";

// 使用结构化输出配置 Agent
ChatClientAgentOptions agentOptions = new(name: AGENT_NAME, instructions: AGENT_INSTRUCTIONS)
{
    ChatOptions = new()
    {
        ResponseFormat = ChatResponseFormatJson.ForJsonSchema(
            schema: AIJsonUtilities.CreateJsonSchema(typeof(TravelPlan)),
            schemaName: "TravelPlan",
            schemaDescription: "Travel Plan with main_task and subtasks")
    }
};

// 创建 AI Agent
AIAgent agent = new OpenAIClient(new ApiKeyCredential(github_token), openAIOptions)
    .GetChatClient(github_model_id)
    .CreateAIAgent(agentOptions);

// 执行规划请求
Console.WriteLine(await agent.RunAsync("为一个四口之家（2个孩子）创建一个从新加坡到墨尔本的旅行计划"));

// 定义结构化输出的数据模型
public class Plan
{
    [JsonPropertyName("assigned_agent")]
    public string? Assigned_agent { get; set; }

    [JsonPropertyName("task_details")]
    public string? Task_details { get; set; }
}

public class TravelPlan
{
    [JsonPropertyName("main_task")]
    public string? Main_task { get; set; }

    [JsonPropertyName("subtasks")]
    public IList<Plan>? Subtasks { get; set; }
}
