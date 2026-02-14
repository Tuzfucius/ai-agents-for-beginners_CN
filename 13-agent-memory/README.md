# 记忆 for AI Agent 
[![Agent 记忆](./images/lesson-13-thumbnail.png)](https://youtu.be/QrYbHesIxpw?si=qNYW6PL3fb3lTPMk)

When discussing the unique benefits of creating AI Agent, two things are mainly discussed: the ability to call 工具s to complete tasks and the the ability to improve over time. 记忆 is at the foundation of creating self-improving Agent that can create better experiences for our users.

In this lesson, we will look at what 记忆 is for AI Agent and how we can manage it and use it for the benefit of our applications.

## 简介

This lesson will cover:

• **Understanding AI Agent 记忆**: What 记忆 is and why it's essential for Agent.

• **Implementing and Storing 记忆**: Practical methods for adding 记忆 capabilities to your AI Agent, focusing on short-term and long-term 记忆.

• **Making AI Agent Self-Improving**: How 记忆 enables Agent to learn from past interactions and improve over time.

## Available Implementations

This lesson includes two comprehensive notebook tutorials:

• **[13-Agent-记忆.ipynb](./13-Agent-记忆.ipynb)**: Implements 记忆 using Mem0 and Azure AI Search with Semantic Kernel 框架

• **[13-Agent-记忆-cognee.ipynb](./13-Agent-记忆-cognee.ipynb)**: Implements structured 记忆 using Cognee, automatically building knowledge graph backed by embeddings, visualizing graph, and intelligent retrieval

## 学习目标

完成本节课后, you will know how to:

• **Differentiate between various types of AI Agent 记忆**, including working, short-term, and long-term 记忆, as well as specialized forms like persona and episodic 记忆.

• **Implement and manage short-term and long-term 记忆 for AI Agent** using the Semantic Kernel 框架, leveraging 工具s like Mem0, Cognee, Whiteboard 记忆, and integrating with Azure AI Search.

• **Understand the principles behind self-improving AI Agent** and how robust 记忆 management systems contribute to continuous learning and adaptation.

## Understanding AI Agent 记忆

At its core, **记忆 for AI Agent refers to the mechanisms that allow them to retain and recall information**. This information can be specific details about a conversation, user preferences, past actions, or even learned 模式s.

Without 记忆, AI applications are often stateless, meaning each interaction starts from scratch. This leads to a repetitive and frustrating user experience where the Agent "forgets" previous context or preferences.

### Why is 记忆 Important?

an Agent's intelligence is deeply tied to its ability to recall and utilize past information. 记忆 allows Agent to be:

• **Reflective**: Learning from past actions and outcomes.

• **Interactive**: Maintaining context over an ongoing conversation.

• **Proactive and Reactive**: Anticipating needs or responding appropriately based on historical data.

• **Autonomous**: Operating more independently by drawing on stored knowledge.

The goal of implementing 记忆 is to make Agent more **reliable and capable**.

### Types of 记忆

#### Working 记忆

Think of this as a piece of scratch paper an Agent uses during a single, ongoing task or thought process. It holds immediate information needed to compute the next step.

For AI Agent, working 记忆 often captures the most relevant information from a conversation, even if the full chat history is long or truncated. It focuses on extracting key elements like requirements, proposals, decisions, and actions.

**Working 记忆 Example**

In a travel booking Agent, working 记忆 might capture the user's current request, such as "I want to book a trip to Paris". This specific requirement is held in the Agent's immediate context to guide the current interaction.

#### Short Term 记忆

This type of 记忆 retains information for the duration of a single conversation or session. It's the context of the current chat, allowing the Agent to refer back to previous turns in the dialogue.

**Short Term 记忆 Example**

If a user asks, "How much would a flight to Paris cost?" and then follows up with "What about accommodation there?", short-term 记忆 ensures the Agent knows "there" refers to "Paris" within the same conversation.

#### Long Term 记忆

This is information that persists across multiple conversations or sessions. It allows Agent to remember user preferences, historical interactions, or general knowledge over extended periods. This is important for personalization.

**Long Term 记忆 Example**

A long-term 记忆 might store that "Ben enjoys skiing and outdoor activities, likes coffee with a mountain view, and wants to avoid advanced ski slopes due to a past injury". This information, learned from previous interactions, influences recommendations in future travel planning sessions, making them highly personalized.

#### Persona 记忆

This specialized 记忆 type helps an Agent develop a consistent "personality" or "persona". It allows the Agent to remember details about itself or its intended role, making interactions more fluid and focused.

**Persona 记忆 Example**
If the travel Agent is designed to be an "expert ski planner," persona 记忆 might reinforce this role, influencing its responses to align with an expert's tone and knowledge.

#### Workflow/Episodic 记忆

This 记忆 stores the sequence of steps an Agent takes during a complex task, including successes and failures. It's like remembering specific "episodes" or past experiences to learn from them.

**Episodic 记忆 Example**

If the Agent attempted to book a specific flight but it failed due to unavailability, episodic 记忆 could record this failure, allowing the Agent to try alternative flights or inform the user about the issue in a more informed way during a subsequent attempt.

#### Entity 记忆

This involves extracting and remembering specific entities (like people, places, or things) and events from conversations. It allows the Agent to build a structured understanding of key elements discussed.

**Entity 记忆 Example**

From a conversation about a past trip, the Agent might extract "Paris," "Eiffel Tower," and "dinner at Le Chat Noir restaurant" as entities. In a future interaction, the Agent could recall "Le Chat Noir" and offer to make a new reservation there.

#### Structured RAG (Retrieval Augmented Generation)

While RAG is a broader technique, "Structured RAG" is highlighted as a powerful 记忆 technology. It extracts dense, structured information from various sources (conversations, emails, images) and uses it to enhance precision, recall, and speed in responses. Unlike classic RAG that relies solely on semantic similarity, Structured RAG works with the inherent structure of information.

**Structured RAG Example**

Instead of just matching keywords, Structured RAG could parse flight details (destination, date, time, airline) from an email and store them in a structured way. This allows precise queries like "What flight did I book to Paris on Tuesday?"

## Implementing and Storing 记忆

Implementing 记忆 for AI Agent involves a systematic process of **记忆 management**, which includes generating, storing, retrieving, integrating, updating, and even "forgetting" (or deleting) information. Retrieval is a particularly crucial aspect.

### Specialized 记忆 工具s

#### Mem0

One way to store and manage Agent 记忆 is using specialized 工具s like Mem0. Mem0 works as a persistent 记忆 layer, allowing Agent to recall relevant interactions, store user preferences and factual context, and learn from successes and failures over time. The idea here is that stateless Agent turn into stateful ones.

It works through a **two-phase 记忆 pipeline: extraction and update**. First, messages added to an Agent's thread are sent to the Mem0 service, which uses a Large Language Model (大型语言模型) to summarize conversation history and extract new memories. Subsequently, an 大型语言模型-driven update phase determines whether to add, modify, or delete these memories, storing them in a hybrid data store that can include vector, graph, and key-value databases. This system also supports various 记忆 types and can incorporate graph 记忆 for managing relationships between entities.

#### Cognee

Another powerful approach is using **Cognee**, an open-source semantic 记忆 for AI Agent that transforms structured and unstructured data into queryable knowledge graphs backed by embeddings. Cognee provides a **dual-store architecture** combining vector similarity search with graph relationships, enabling Agent to understand not just what information is similar, but how concepts relate to each other.

It excels at **hybrid retrieval** that blends vector similarity, graph structure, and 大型语言模型 reasoning - from raw chunk lookup to graph-aware question answering. The system maintains **living 记忆** that evolves and grows while remaining queryable as one connected graph, supporting both short-term session context and long-term persistent 记忆.

The Cognee notebook tutorial ([13-Agent-记忆-cognee.ipynb](./13-Agent-记忆-cognee.ipynb)) demonstrates building this unified 记忆 layer, with practical examples of ingesting diverse data sources, visualizing the knowledge graph, and querying with different search strategies tailored to specific Agent needs.

### Storing 记忆 with RAG

Beyond specialized 记忆 工具s like mem0 , you can leverage robust search services like **Azure AI Search as a backend for storing and retrieving memories**, especially for structured RAG.

This allows you to ground your Agent's responses with your own data, ensuring more relevant and accurate answers. Azure AI Search can be used to store user-specific travel memories, product catalogs, or any other domain-specific knowledge.

Azure AI Search supports capabilities like **Structured RAG**, which excels at extracting and retrieving dense, structured information from large datasets like conversation histories, emails, or even images. This provides "superhuman precision and recall" compared to traditional text chunking and embedding approaches.

## Making AI Agent Self-Improve

A common 模式 for self-improving Agent involves introducing a **"knowledge Agent"**. This separate Agent observes the main conversation between the user and the primary Agent. Its role is to:

1. **Identify valuable information**: Determine if any part of the conversation is worth saving as general knowledge or a specific user preference.

2. **Extract and summarize**: Distill the essential learning or preference from the conversation.

3. **Store in a knowledge base**: Persist this extracted information, often in a vector database, so it can be retrieved later.

4. **Augment future queries**: When the user initiates a new query, the knowledge Agent retrieves relevant stored information and appends it to the user's prompt, providing crucial context to the primary Agent (similar to RAG).

### Optimizations for 记忆

• **Latency Management**: To avoid slowing down user interactions, a cheaper, faster model can be used initially to quickly check if information is valuable to store or retrieve, only invoking the more complex extraction/retrieval process when necessary.

• **Knowledge Base Maintenance**: For a growing knowledge base, less frequently used information can be moved to "cold storage" to manage costs.

## Got More Questions About Agent 记忆?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.
