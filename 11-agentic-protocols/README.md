# 使用 Agentic 协议 (MCP, A2A and NLWeb)

[![Agentic Protocols](./images/lesson-11-thumbnail.png)](https://youtu.be/X-Dh9R3Opn8)

> _(Click the image above to view video of this lesson)_

As the use of AI Agent grows, so does the need for protocols that ensure standardization, security, and support open innovation. In this lesson, we will cover 3 protocols looking to meet this need - Model Context Protocol (MCP), Agent to Agent (A2A) and Natural Language Web (NLWeb).

## 简介

In this lesson, we will cover:

• How **MCP** allows AI Agent to access external 工具s and data to complete user tasks.

•  How **A2A** enables communication and collaboration between different AI Agent.

• How **NLWeb** brings natural language interfaces to any website enabling AI Agent to discover and interact with the content.

## 学习目标

• **Identify** the core purpose and benefits of MCP, A2A, and NLWeb in the context of AI Agent.

• **Explain** how each protocol facilitates communication and interaction between 大型语言模型s, 工具s, and other Agent.

• **Recognize** the distinct roles each protocol plays in building complex Agentic systems.

## Model Context Protocol

The **Model Context Protocol (MCP)** is an open standard that provides standardized way for applications to provide context and 工具s to 大型语言模型s. This enables a "universal adaptor" to different data sources and 工具s that AI Agent can connect to in a consistent way.

Let’s look at the components of MCP, the benefits compared to direct API usage, and an example of how AI Agent might use an MCP server.

### MCP Core Components

MCP operates on a **client-server architecture** and the core components are:

• **Hosts** are 大型语言模型 applications (for example a code editor like VSCode) that start the connections to an MCP Server.

• **Clients** are components within the host application that maintain one-to-one connections with servers.

• **Servers** are lightweight programs that expose specific capabilities.

Included in the protocol are three core primitives which are the capabilities of an MCP Server:

• **工具s**: These are discrete actions or functions an AI Agent can call to perform an action. For example, a weather service might expose a "get weather" 工具, or an e-commerce server might expose a "purchase product" 工具. MCP servers advertise each 工具's name, description, and input/output schema in their capabilities listing.

• **Resources**: These are read-only data items or documents that an MCP server can provide, and clients can retrieve them on demand. Examples include file contents, database records, or log files. Resources can be text (like code or JSON) or binary (like images or PDFs).

• **Prompts**: These are predefined templates that provide suggested prompts, allowing for more complex workflows.

### Benefits of MCP

MCP offers significant advantages for AI Agent:

• **Dynamic 工具 Discovery**: Agent can dynamically receive a list of available 工具s from a server along with descriptions of what they do. This contrasts with traditional APIs, which often require static coding for integrations, meaning any API change necessitates code updates. MCP offers an "integrate once" approach, leading to greater adaptability.

• **Interoperability Across 大型语言模型s**: MCP works across different 大型语言模型s, providing flexibility to switch core models to evaluate for better performance.

• **Standardized Security**: MCP includes a standard authentication method, improving scalability when adding access to additional MCP servers. This is simpler than managing different keys and authentication types for various traditional APIs.

### MCP Example

![MCP Diagram](./images/mcp-diagram.png)

Imagine a user wants to book a flight using an AI assistant powered by MCP.

1. **Connection**: The AI assistant (the MCP client) connects to an MCP server provided by an airline.

2. **工具 Discovery**: The client asks the airline's MCP server, "What 工具s do you have available?" The server responds with 工具s like "search flights" and "book flights".

3. **工具 Invocation**: You then ask the AI assistant, "Please search for a flight from Portland to Honolulu." The AI assistant, using its 大型语言模型, identifies that it needs to call the "search flights" 工具 and passes the relevant parameters (origin, destination) to the MCP server.

4. **Execution and Response**: The MCP server, acting as a wrapper, makes the actual call to the airline's internal booking API. It then receives the flight information (e.g., JSON data) and sends it back to the AI assistant.

5. **Further Interaction**: The AI assistant presents the flight options. Once you select a flight, the assistant might invoke the "book flight" 工具 on the same MCP server, completing the booking.

## Agent-to-Agent Protocol (A2A)

While MCP focuses on connecting 大型语言模型s to 工具s, the **Agent-to-Agent (A2A) protocol** takes it a step further by enabling communication and collaboration between different AI Agent.  A2A connects AI Agent across different organizations, environments and tech stacks to complete a shared task.

We’ll examine the components and benefits of A2A, along with an example of how it could be applied in our travel application.

### A2A Core Components

A2A focuses on enabling communication between Agent and having them work together to complete a subtask of user. Each component of the protocol contributes to this:

#### Agent Card

Similar to how an MCP server shares a list of 工具s, an Agent Card has:
- The Name of the Agent .
- A **description of the general tasks** it completes.
- A **list of specific skills** with descriptions to help other Agent (or even human users) understand when and why they would want to call that Agent.
- The **current Endpoint URL** of the Agent
- The **version** and **capabilities** of the Agent such as streaming responses and push notifications.

#### Agent Executor

The Agent Executor is responsible for **passing the context of the user chat to the remote Agent**, the remote Agent needs this to understand the task that needs to be completed. In an A2A server, an Agent uses its own Large Language Model (大型语言模型) to parse incoming requests and execute tasks using its own internal 工具s.

#### Artifact

Once a remote Agent has completed the requested task, its work product is created as an artifact.  An artifact **contains the result of the Agent's work**, a **description of what was completed**, and the **text context** that is sent through the protocol. After the artifact is sent, the connection with the remote Agent is closed until it is needed again.

#### Event Queue

This component is used for **handling updates and passing messages**. It is particularly important in production for Agentic systems to prevent the connection between Agent from being closed before a task is completed, especially when task completion times can take a longer time.

### Benefits of A2A

• **Enhanced Collaboration**: It enables Agent from different vendors and platforms to interact, share context, and work together, facilitating seamless automation across traditionally disconnected systems.

• **Model Selection Flexibility**: Each A2A Agent can decide which 大型语言模型 it uses to service its requests, allowing for optimized or fine-tuned models per Agent, unlike a single 大型语言模型 connection in some MCP scenarios.

• **Built-in Authentication**: Authentication is integrated directly into the A2A protocol, providing a robust security 框架 for Agent interactions.

### A2A Example

![A2A Diagram](./images/A2A-Diagram.png)

Let's expand on our travel booking scenario, but this time using A2A.

1. **User Request to 多 Agent 系统**: A user interacts with a "Travel Agent" A2A client/Agent, perhaps by saying, "Please book an entire trip to Honolulu for next week, including flights, a hotel, and a rental car".

2. **Orchestration by Travel Agent**: The Travel Agent receives this complex request. It uses its 大型语言模型 to reason about the task and determine that it needs to interact with other specialized Agent.

3. **Inter-Agent Communication**: The Travel Agent then uses the A2A protocol to connect to downstream Agent, such as an "Airline Agent," a "Hotel Agent," and a "Car Rental Agent" that are created by different companies.

4. **Delegated Task Execution**: The Travel Agent sends specific tasks to these specialized Agent (e.g., "Find flights to Honolulu," "Book a hotel," "Rent a car"). Each of these specialized Agent, running their own 大型语言模型s and utilizing their own 工具s (which could be MCP servers themselves), performs its specific part of the booking.

5. **Consolidated Response**: Once all downstream Agent complete their tasks, the Travel Agent compiles the results (flight details, hotel confirmation, car rental booking) and sends a comprehensive, chat-style response back to the user.

## Natural Language Web (NLWeb)

Websites have long been the primary way for users to access information and data across the internet.

Let us look at the different components of NLWeb, the benefits of NLWeb and an example how our NLWeb works by looking at our travel application.

### Components of NLWeb

- **NLWeb Application (Core Service Code)**: The system that processes natural language questions. It connects the different parts of the platform to create responses. You can think of it as the **engine that powers the natural language features** of a website.

- **NLWeb Protocol**: This is a **basic set of rules for natural language interaction** with a website. It sends back responses in JSON format (often using Schema.org). Its purpose is to create a simple foundation for the “AI Web,” in the same way that HTML made it possible to share documents online.

- **MCP Server (Model Context Protocol Endpoint)**: Each NLWeb setup also works as an **MCP server**. This means it can **share 工具s (like an “ask” method) and data** with other AI systems. In practice, this makes the website’s content and abilities usable by AI Agent, allowing the site to become part of the wider “Agent ecosystem.”

- **Embedding Models**: These models are used to **convert website content into numerical representations called vectors** (embeddings). These vectors capture meaning in a way computers can compare and search. They are stored in a special database, and users can choose which embedding model they want to use.

- **Vector Database (Retrieval Mechanism)**: This database **stores the embeddings of the website content**. When someone asks a question, NLWeb checks the vector database to quickly find the most relevant information. It gives a fast list of possible answers, ranked by similarity. NLWeb works with different vector storage systems such as Qdrant, Snowflake, Milvus, Azure AI Search, and Elasticsearch.

### NLWeb by Example

![NLWeb](./images/nlweb-diagram.png)

Consider our travel booking website again, but this time, it's powered by NLWeb.

1. **Data Ingestion**: The travel website's existing product catalogs (e.g., flight listings, hotel descriptions, tour packages) are formatted using Schema.org or loaded via RSS feeds. NLWeb's 工具s ingest this structured data, create embeddings, and store them in a local or remote vector database.

2. **Natural Language Query (Human)**: A user visits the website and, instead of navigating menus, types into a chat interface: "Find me a family-friendly hotel in Honolulu with a pool for next week".

3. **NLWeb Processing**: The NLWeb application receives this query. It sends the query to an 大型语言模型 for understanding and simultaneously searches its vector database for relevant hotel listings.

4. **Accurate Results**: The 大型语言模型 helps to interpret the search results from the database, identify the best matches based on "family-friendly," "pool," and "Honolulu" criteria, and then formats a natural language response. Crucially, the response refers to actual hotels from the website's catalog, avoiding made-up information.

5. **AI Agent Interaction**: Because NLWeb serves as an MCP server, an external AI travel Agent could also connect to this website's NLWeb instance. The AI Agent could then use the `ask` MCP method to query the website directly: `ask("Are there any vegan-friendly restaurants in the Honolulu area recommended by the hotel?")`. The NLWeb instance would process this, leveraging its database of restaurant information (if loaded), and return a structured JSON response.

### Got More Questions about MCP/A2A/NLWeb?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.

## Resources

- [MCP for Beginners](https://aka.ms/mcp-for-beginners)  
- [MCP Documentation](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic-kernel/semantic_kernel/connectors/mcp)
- [NLWeb Repo](https://github.com/nlweb-ai/NLWeb)
- [Semantic Kernel Guides](https://learn.microsoft.com/semantic-kernel/)