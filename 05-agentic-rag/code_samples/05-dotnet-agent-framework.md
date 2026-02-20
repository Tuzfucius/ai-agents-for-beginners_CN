# 🔍 使用 Azure AI Foundry 的企业级 RAG (.NET)

## 📋 学习目标

本教程演示了如何使用 Microsoft Agent Framework for .NET 与 Azure AI Foundry 构建企业级检索增强生成（RAG）系统。你将学习创建生产就绪的代理，这些代理可以搜索文档并提供准确、具有上下文感知的响应，同时具备企业级安全性和可扩展性。

**你将构建的企业级 RAG 能力：**
- 📚 **文档智能**：使用 Azure AI 服务进行高级文档处理
- 🔍 **语义搜索**：具有企业功能的高性能向量搜索
- 🛡️ **安全集成**：基于角色的访问和数据保护模式
- 🏢 **可扩展架构**：带有监控的生产就绪 RAG 系统

## 🎯 企业级 RAG 架构

### 核心企业组件
- **Azure AI Foundry**：具有安全性和合规性的托管企业 AI 平台
- **持久化代理**：具有对话历史和上下文管理的有状态代理
- **向量存储管理**：企业级文档索引和检索
- **身份集成**：Azure AD 认证和基于角色的访问控制

### .NET 企业级优势
- **类型安全**：RAG 操作和数据结构的编译时验证
- **异步性能**：非阻塞文档处理和搜索操作
- **内存管理**：大型文档集合的高效资源利用
- **集成模式**：具有依赖注入的原生 Azure 服务集成

## 🏗️ 技术架构

### 企业级 RAG 流程
```
文档上传 → 安全验证 → 向量处理 → 索引创建
                      ↓                    ↓                  ↓
用户查询 → 认证 → 语义搜索 → 上下文排序 → AI 响应
```

### 核心 .NET 组件
- **Azure.AI.Agents.Persistent**：带状态持久化的企业级代理管理
- **Azure.Identity**：用于安全 Azure 服务访问的集成认证
- **Microsoft.Agents.AI.AzureAI**：Azure 优化的代理框架实现
- **System.Linq.Async**：高性能异步 LINQ 操作

## 🔧 企业级特性与优势

### 安全与合规
- **Azure AD 集成**：企业身份管理和认证
- **基于角色的访问**：文档访问和操作的细粒度权限
- **数据保护**：敏感文档的静态和传输加密
- **审计日志**：综合活动跟踪以满足合规要求

### 性能与可扩展性
- **连接池**：高效的 Azure 服务连接管理
- **异步处理**：高吞吐量场景的非阻塞操作
- **缓存策略**：频繁访问文档的智能缓存
- **负载均衡**：大规模部署的分布式处理

### 管理与监控
- **健康检查**：RAG 系统组件的内置监控
- **性能指标**：搜索质量和响应时间的详细分析
- **错误处理**：带重试策略的综合异常管理
- **配置管理**：带验证的环境特定设置

## ⚙️ 前置条件与设置

**开发环境：**
- .NET 9.0 SDK 或更高版本
- Visual Studio 2022 或带 C# 扩展的 VS Code
- 具有 AI Foundry 访问权限的 Azure 订阅

**所需 NuGet 包：**
```xml
<PackageReference Include="Microsoft.Extensions.AI" Version="9.9.0" />
<PackageReference Include="Azure.AI.Agents.Persistent" Version="1.2.0-beta.5" />
<PackageReference Include="Azure.Identity" Version="1.15.0" />
<PackageReference Include="System.Linq.Async" Version="6.0.3" />
<PackageReference Include="DotNetEnv" Version="3.1.1" />
```

**Azure 认证设置：**
```bash
# 安装 Azure CLI 并进行认证
az login
az account set --subscription "your-subscription-id"
```

**环境配置：**
* Azure AI Foundry 配置（通过 Azure CLI 自动处理）
* 确保已通过正确的 Azure 订阅进行认证

## 📊 企业级 RAG 模式

### 文档管理模式
- **批量上传**：大型文档集合的高效处理
- **增量更新**：实时文档添加和修改
- **版本控制**：文档版本管理和变更跟踪
- **元数据管理**：丰富的文档属性和分类法

### 搜索与检索模式
- **混合搜索**：结合语义和关键词搜索以获得最佳结果
- **分面搜索**：多维过滤和分类
- **相关性调优**：针对领域需求的自定义评分算法
- **结果排序**：带有业务逻辑集成的高级排序

### 安全模式
- **文档级安全**：每个文档的细粒度访问控制
- **数据分类**：自动敏感度标签和保护
- **审计跟踪**：所有 RAG 操作的综合日志
- **隐私保护**：PII 检测和编辑能力

## 🔒 企业级安全特性

### 认证与授权
```csharp
// Azure AD 集成认证
var credential = new AzureCliCredential();
var agentsClient = new PersistentAgentsClient(endpoint, credential);

// 基于角色的访问验证
if (!await ValidateUserPermissions(user, documentId))
{
    throw new UnauthorizedAccessException("Insufficient permissions");
}
```

### 数据保护
- **加密**：文档和搜索索引的端到端加密
- **访问控制**：与 Azure AD 集成用于用户和组权限
- **数据驻留**：用于合规的地理数据位置控制
- **备份与恢复**：自动备份和灾难恢复能力

## 📈 性能优化

### 异步处理模式
```csharp
// 高效的异步文档处理
await foreach (var document in documentStream.AsAsyncEnumerable())
{
    await ProcessDocumentAsync(document, cancellationToken);
}
```

### 内存管理
- **流式处理**：无需内存问题即可处理大型文档
- **资源池化**：昂贵资源的高效重用
- **垃圾回收**：优化的内存分配模式
- **连接管理**：正确的 Azure 服务连接生命周期

### 缓存策略
- **查询缓存**：缓存频繁执行的搜索
- **文档缓存**：热门文档的内存缓存
- **索引缓存**：优化的向量索引缓存
- **结果缓存**：生成响应的智能缓存

## 📊 企业用例

### 知识管理
- **企业 Wiki**：跨公司知识库的智能搜索
- **政策与程序**：自动化合规性和程序指导
- **培训材料**：智能学习和发展协助
- **研究数据库**：学术和研究论文分析系统

### 客户支持
- **支持知识库**：自动客户服务响应
- **产品文档**：智能产品信息检索
- **故障排除指南**：上下文问题解决协助
- **FAQ 系统**：从文档集合动态生成 FAQ

### 法规合规
- **法律文档分析**：合同和法律文档智能
- **合规监控**：自动化法规合规检查
- **风险评估**：基于文档的风险分析和报告
- **审计支持**：审计的智能文档发现

## 🚀 生产部署

### 监控与可观测性
- **Application Insights**：详细的遥感和性能监控
- **自定义指标**：特定业务的 KPI 跟踪和警报
- **分布式跟踪**：跨服务的端到端请求跟踪
- **健康仪表板**：实时系统健康和性能可视化

### 可扩展性与可靠性
- **自动扩展**：根据负载和性能指标自动扩展
- **高可用性**：具有故障转移能力的多区域部署
- **负载测试**：企业负载条件下的性能验证
- **灾难恢复**：自动备份和恢复程序

准备好构建能够大规模处理敏感文档的企业级 RAG 系统了吗？让我们为企业构建智能知识系统！🏢📖✨

## 代码实现

本课程的完整工作代码示例在 `05-dotnet-agent-framework.cs` 中提供。

运行示例：

```bash
# 使脚本可执行（Linux/macOS）
chmod +x 05-dotnet-agent-framework.cs

# 运行 .NET 单文件应用
./05-dotnet-agent-framework.cs
```

或直接使用 `dotnet run`：

```bash
dotnet run 05-dotnet-agent-framework.cs
```

代码演示了：

1. **包安装**：安装 Azure AI Agents 所需的 NuGet 包
2. **环境配置**：加载 Azure AI Foundry 端点和模型设置
3. **文档上传**：上传文档进行 RAG 处理
4. **向量存储创建**：创建用于语义搜索的向量存储
5. **代理配置**：设置具有文件搜索功能的 AI 代理
6. **查询执行**：针对上传的文档运行查询
