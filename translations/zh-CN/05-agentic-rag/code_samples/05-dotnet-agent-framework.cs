#!/usr/bin/dotnet run
#:package Microsoft.Extensions.AI@9.9.1
#:package Azure.AI.Agents.Persistent@1.2.0-beta.5
#:package Azure.Identity@1.15.0
#:package System.Linq.Async@6.0.3
#:package Microsoft.Agents.AI.AzureAI@1.0.0-preview.251001.3
#:package Microsoft.Agents.AI@1.0.0-preview.251001.3
#:package DotNetEnv@3.1.1

using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Agents.AI;
using DotNetEnv;

// 加载环境变量
Env.Load("../../../.env");

// 获取 Azure AI Foundry 配置
var azure_foundry_endpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT") ?? throw new InvalidOperationException("AZURE_AI_PROJECT_ENDPOINT is not set.");
var azure_foundry_model_id = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-4.1-mini";

// 定义文档路径
string pdfPath = "./document.md";

// 辅助函数：打开文件流
async Task<Stream> OpenImageStreamAsync(string path)
{
    return await Task.Run(() => File.OpenRead(path));
}

// 打开文档流
var pdfStream = await OpenImageStreamAsync(pdfPath);

// 创建持久化 Agents 客户端
var persistentAgentsClient = new PersistentAgentsClient(azure_foundry_endpoint, new AzureCliCredential());

// 上传文件
PersistentAgentFileInfo fileInfo = await persistentAgentsClient.Files.UploadFileAsync(pdfStream, PersistentAgentFilePurpose.Agents, "demo.md");

// 创建向量存储
PersistentAgentsVectorStore fileStore =
    await persistentAgentsClient.VectorStores.CreateVectorStoreAsync(
        [fileInfo.Id],
        metadata: new Dictionary<string, string>() { { "agentkey", bool.TrueString } });

// 创建 RAG Agent
PersistentAgent agentModel = await persistentAgentsClient.Administration.CreateAgentAsync(
    azure_foundry_model_id,
    name: "DotNetRAGAgent",
    tools: [new FileSearchToolDefinition()],
    instructions: """
        你是一个 AI 助手，旨在仅使用从提供的文档中检索的信息来回答用户问题。

        - 如果用户的问题无法使用检索到的上下文回答，你必须明确回复：
        "抱歉，上传的文档中没有包含回答该问题所需的信息。"
        - 不要根据一般知识或推理来回答。不要做假设或生成假设性的解释。
        - 不要提供未明确基于上传文件内容的定义、教程或评论。
        - 如果用户问的问题是"什么是神经网络？"，而上传的文档中没有讨论这个问题，请按照上述指示回复。
        - 对于文档中确实有相关内容的问题（例如，Contoso 的旅行保险覆盖范围），请准确回复，并明确引用文档。

        你必须表现得好像除了从上传文档中检索的内容之外，没有外部知识。
        """,
    toolResources: new()
    {
        FileSearch = new()
        {
            VectorStoreIds = { fileStore.Id },
        }
    },
    metadata: new Dictionary<string, string>() { { "agentkey", bool.TrueString } });

// 获取 AI Agent
AIAgent agent = await persistentAgentsClient.GetAIAgentAsync(agentModel.Id);

// 创建新线程
AgentThread thread = agent.GetNewThread();

// 运行查询
Console.WriteLine(await agent.RunAsync("你能解释一下 Contoso 的旅行保险覆盖范围吗？", thread));
