# 🤝 企业级多代理工作流系统 (.NET)

## 📋 学习目标

本教程演示了如何使用 Microsoft Agent Framework for .NET 与 GitHub Models 构建复杂的企业级多代理系统。你将学习通过结构化工作流协调多个专业代理协同工作，充分利用 .NET 的企业级特性来实现生产就绪的解决方案。

**你将构建的企业级多代理能力：**
- 👥 **代理协作**：具有编译时验证的类型安全代理协调
- 🔄 **工作流编排**：使用 .NET 异步模式的声明式工作流定义
- 🎭 **角色专业化**：强类型的代理个性和专业领域
- 🏢 **企业集成**：带有监控和错误处理的生产就绪模式

## ⚙️ 前置条件与设置

**开发环境：**
- .NET 9.0 SDK 或更高版本
- Visual Studio 2022 或带 C# 扩展的 VS Code
- Azure 订阅（用于持久化代理）

**所需 NuGet 包：**
```xml
<PackageReference Include="Microsoft.Extensions.AI.Abstractions" Version="9.9.0" />
<PackageReference Include="Azure.AI.Agents.Persistent" Version="1.2.0-beta.4" />
<PackageReference Include="Azure.Identity" Version="1.15.0" />
<PackageReference Include="System.Linq.Async" Version="6.0.3" />
<PackageReference Include="Microsoft.Extensions.AI" Version="9.8.0" />
<PackageReference Include="DotNetEnv" Version="3.1.1" />
<PackageReference Include="Microsoft.Extensions.AI.OpenAI" Version="9.9.0-preview.1.25458.4" />
```

## 代码示例

本课程的完整工作代码在随附的 C# 文件中提供：[`08-dotnet-agent-framework.cs`](./08-dotnet-agent-framework.cs)

运行示例：

```bash
# 使文件可执行（Linux/macOS）
chmod +x 08-dotnet-agent-framework.cs

# 运行示例
./08-dotnet-agent-framework.cs
```

或使用 .NET CLI：

```bash
dotnet run 08-dotnet-agent-framework.cs
```

## 本示例演示的内容

这个多代理工作流系统创建了一个酒店旅行推荐服务，包含两个专业代理：

1. **前台代理**：提供活动和地点推荐的旅行代理
2. **礼宾代理**：审查推荐以确保 authentic、非旅游化的体验

代理在工作流中协同工作：
- 前台代理接收初始旅行请求
- 礼宾代理审查并优化推荐
- 工作流实时流式传输响应

## 关键概念

### 代理协调
示例演示了使用 Microsoft Agent Framework 进行具有编译时验证的类型安全代理协调。

### 工作流编排
使用 .NET 异步模式的声明式工作流定义，将多个代理连接到一个管道中。

### 流式响应
使用异步可枚举和事件驱动架构实现代理响应的实时流式传输。

### 企业集成
展示生产就绪模式，包括：
- 环境变量配置
- 安全凭证管理
- 错误处理
- 异步事件处理
