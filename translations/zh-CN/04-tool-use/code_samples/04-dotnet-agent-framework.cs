#!/usr/bin/dotnet run

#:package Microsoft.Extensions.AI@10.*
#:package Microsoft.Extensions.AI.OpenAI@10.*-*
#:package Microsoft.Agents.AI.OpenAI@1.*-*

using System.ClientModel;
using System.ComponentModel;
using System.Text.Json;

using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

using OpenAI;

// ============================================================================
// TOOL USE DESIGN PATTERN DEMONSTRATION
// ============================================================================
// This sample demonstrates the key concepts from the Tool Use lesson:
// 1. FUNCTION SCHEMAS: Clear descriptions and typed parameters
// 2. MULTIPLE TOOLS: Agent selects the right tool for each task
// 3. TOOL COMPOSITION: Tools can work together to solve complex requests
// 4. PARAMETER HANDLING: Functions with different parameter types
// ============================================================================

// ----------------------------------------------------------------------------
// TOOL 1: 随机目的地生成器（无参数）
// ----------------------------------------------------------------------------
// 演示：无参数的简单工具
[Description("当用户未指定目的地时，提供随机的度假目的地。")]
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
    
    Console.WriteLine($"\n[工具调用] GetRandomDestination() -> {destinations[index]}");
    return destinations[index];
}

// ----------------------------------------------------------------------------
// TOOL 2: 天气查询（单参数）
// ----------------------------------------------------------------------------
// 演示：带必需参数的工具 - LLM 必须从用户消息中提取位置并传递给此函数
[Description("获取指定位置的当前天气状况。在规划活动或打包建议时使用。")]
static string GetWeather(
    [Description("要获取天气的城市和国家，例如 'Paris, France'")] string location)
{
    // 用于演示的模拟天气数据
    var weatherConditions = new Dictionary<string, (string condition, int tempC, int tempF)>
    {
        { "paris", ("多云", 18, 64) },
        { "tokyo", ("晴", 24, 75) },
        { "new york", ("雨", 15, 59) },
        { "sydney", ("晴", 28, 82) },
        { "rome", ("晴朗", 22, 72) },
        { "barcelona", ("晴", 26, 79) },
        { "cape town", ("多风", 19, 66) },
        { "rio", ("炎热潮湿", 32, 90) },
        { "bangkok", ("热带", 33, 91) },
        { "vancouver", ("阴", 12, 54) }
    };

    var locationLower = location.ToLower();
    foreach (var (key, weather) in weatherConditions)
    {
        if (locationLower.Contains(key))
        {
            var result = $"{location} 天气：{weather.condition}，{weather.tempC}°C ({weather.tempF}°F)";
            Console.WriteLine($"\n[工具调用] GetWeather(\"{location}\") -> {result}");
            return result;
        }
    }

    var defaultResult = $"{location} 天气：温和条件，约 20°C (68°F)";
    Console.WriteLine($"\n[工具调用] GetWeather(\"{location}\") -> {defaultResult}");
    return defaultResult;
}

// ----------------------------------------------------------------------------
// TOOL 3: 目的地信息（多参数）
// ----------------------------------------------------------------------------
// 演示：带多个参数的工具，包括类似枚举的类别
[Description("获取目的地的详细信息，包括景点、美食和旅行提示。在选择目的地后使用此工具提供丰富的细节。")]
static string GetDestinationInfo(
    [Description("要获取信息的城市目的地")] string destination,
    [Description("信息类别：'attractions'、'cuisine'、'tips' 或 'all'")] string category = "all")
{
    Console.WriteLine($"\n[工具调用] GetDestinationInfo(\"{destination}\", \"{category}\")");
    
    // 模拟目的地数据
    var info = new Dictionary<string, Dictionary<string, string>>
    {
        { "paris", new() {
            { "attractions", "埃菲尔铁塔、卢浮宫、巴黎圣母院、香榭丽舍大街" },
            { "cuisine", "牛角面包、法式洋葱汤、红酒炖鸡、马卡龙" },
            { "tips", "地铁很高效，提前预约博物馆，给小费 10-15%" }
        }},
        { "tokyo", new() {
            { "attractions", "浅草寺、涩谷十字路口、东京塔、秋叶原" },
            { "cuisine", "寿司、拉面、天妇罗、和牛" },
            { "tips", "购买 Suica 卡，鞠躬问候，室内脱鞋" }
        }},
        { "rome", new() {
            { "attractions", "斗兽场、梵蒂冈、特莱维喷泉、万神殿" },
            { "cuisine", "罗马式培根意粉、切片披萨、提拉米苏" },
            { "tips", "提前预约梵蒂冈，携带水瓶，午休时间 13:00-16:00" }
        }}
    };

    var destLower = destination.ToLower();
    foreach (var (key, data) in info)
    {
        if (destLower.Contains(key))
        {
            if (category.ToLower() == "all")
            {
                return JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
            }
            if (data.TryGetValue(category.ToLower(), out var value))
            {
                return $"{destination} 的{category}：{value}";
            }
        }
    }

    return $"关于 {destination} 的信息：一个拥有丰富文化和体验的绝佳目的地。";
}

// ----------------------------------------------------------------------------
// TOOL 4: 行程费用估算（数值参数）
// ----------------------------------------------------------------------------
// 演示：带数值参数的工具用于计算
[Description("根据目的地、时长和预算等级估算总行程费用。返回费用明细。")]
static string EstimateTripCost(
    [Description("目的地城市")] string destination,
    [Description("旅行天数")] int days,
    [Description("预算等级：'budget'、'moderate' 或 'luxury'")] string budgetLevel = "moderate")
{
    Console.WriteLine($"\n[工具调用] EstimateTripCost(\"{destination}\", {days}, \"{budgetLevel}\")");
    
    var dailyRates = new Dictionary<string, int>
    {
        { "budget", 100 },
        { "moderate", 250 },
        { "luxury", 500 }
    };

    var rate = dailyRates.GetValueOrDefault(budgetLevel.ToLower(), 250);
    var accommodation = rate * days;
    var food = (rate / 2) * days;
    var activities = (rate / 3) * days;
    var total = accommodation + food + activities;

    return $"""
        {destination}（{days} 天，{budgetLevel} 级别）行程费用估算：
        - 住宿：${accommodation}
        - 餐饮：${food}
        - 活动：${activities}
        - 预计总计：${total}
        """;
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
// AGENT INSTRUCTIONS - 工具使用专家
// ============================================================================
var AGENT_INSTRUCTIONS = """
你是一个可以访问多个专业工具的旅行规划 AI Agent。

## 可用工具

你可以适当使用这些工具：

1. **GetRandomDestination**：推荐随机目的地（无需参数）
2. **GetWeather**：获取某地天气（需要：location）
3. **GetDestinationInfo**：获取景点/美食/提示（需要：destination，可选：category）
4. **EstimateTripCost**：计算费用（需要：destination、days，可选：budgetLevel）

## 工具使用指南

- **链接工具**以获得全面的响应（例如：目的地 → 天气 → 信息 → 费用）
- 从用户消息中**提取参数**传递给工具
- 根据用户询问的内容**选择合适的工具**
- 当用户要求"完整行程规划"时，使用多个工具

## 响应格式

使用工具后，将信息综合成有帮助、结构良好的响应。
始终提及你使用了哪些工具，以便用户了解 Agent 的能力。
""";

// 使用多个工具创建 AI Agent
// 这展示了具有各种工具类型的 Tool Use 设计模式
AIAgent agent = openAIClient
    .GetChatClient(github_model_id)
    .AsIChatClient()
    .CreateAIAgent(
        name: AGENT_NAME,
        instructions: AGENT_INSTRUCTIONS,
        tools: [
            AIFunctionFactory.Create(GetRandomDestination),
            AIFunctionFactory.Create(GetWeather),
            AIFunctionFactory.Create(GetDestinationInfo),
            AIFunctionFactory.Create(EstimateTripCost)
        ]
    );

// 创建对话线程
AgentThread thread = agent.GetNewThread();

// ============================================================================
// 演示 1：工具选择 - Agent 选择正确的工具
// ============================================================================
Console.WriteLine("=== 工具使用设计模式演示 ===\n");
Console.WriteLine("--- 演示 1：工具选择 ---");
Console.WriteLine("用户：东京的天气怎么样？\n");
Console.WriteLine("Agent 回复：");

await foreach (var update in agent.RunStreamingAsync("东京的天气怎么样？", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}

Console.WriteLine("\n");

// ============================================================================
// 演示 2：参数化工具调用
// ============================================================================
Console.WriteLine("--- 演示 2：带多个参数的参数化工具 ---");
Console.WriteLine("用户：去罗马玩 5 天豪华游需要多少钱？\n");
Console.WriteLine("Agent 回复：");

await foreach (var update in agent.RunStreamingAsync("去罗马玩 5 天豪华游需要多少钱？", thread))
{
    await Task.Delay(10);
    Console.Write(update);
}

Console.WriteLine("\n");

// ============================================================================
// 演示 3：工具组合 - 多个工具处理复杂请求
// ============================================================================
Console.WriteLine("--- 演示 3：工具组合 ---");
Console.WriteLine("用户：帮我规划一个完整行程 - 推荐一个目的地，给我所有详情，包括天气和 3 天中等预算的费用。\n");
Console.WriteLine("Agent 回复：");

await foreach (var update in agent.RunStreamingAsync(
    "帮我规划一个完整行程 - 推荐一个目的地，给我所有详情，包括天气和 3 天中等预算的费用。", 
    thread))
{
    await Task.Delay(10);
    Console.Write(update);
}
