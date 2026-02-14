# 上下文工程 for AI Agent

[![上下文工程](./images/lesson-12-thumbnail.png)](https://youtu.be/F5zqRV7gEag)

> _(Click the image above to view video of this lesson)_

Understanding the complexity of the application you are building an AI Agent for is important to making a reliable one. We need to build AI Agent that effectively manage information to address complex needs beyond prompt engineering.

In this lesson, we will look at what context engineering is and its role in building AI Agent.

## 简介

This lesson will cover:

• **What 上下文工程 is** and why it's different from prompt engineering.

• **Strategies for effective 上下文工程**, including how to write, select, compress, and isolate information.

• **Common Context Failures** that can derail your AI Agent and how to fix them.

## 学习目标

完成本节课后, you will know understand how to:

• **Define context engineering** and differentiate it from prompt engineering.

• **Identify the key components of context** in Large Language Model (大型语言模型) applications.

• **Apply strategies for writing, selecting, compressing, and isolating context** to improve Agent performance.

• **Recognize common context failures** such as poisoning, distraction, confusion, and clash, and implement mitigation techniques.

## 什么是 is 上下文工程?

For AI Agent, context is what drives the planning of an AI Agent to take certain actions. 上下文工程 is the practice of making sure the AI Agent has the right information to complete the next step of the task. The context window is limited in size, so as Agent builders we need to build systems and processes to manage adding, removing, and condensing the information in the context window.

### Prompt Engineering vs 上下文工程

Prompt engineering is focused on a single set of static instructions to effectively guide the AI Agent with a set of rules.  Context engineering is how to manage a dynamic set of information, including the initial prompt, to ensure that the AI Agent has what it needs over time. The main idea around context engineering is to make this process repeatable and reliable.

### Types of Context

[![Types of Context](./images/context-types.png)](https://youtu.be/F5zqRV7gEag)

It is important to remember that context is not just one thing. The information  that the AI Agent needs can come from a variety of different sources and it is up to us to ensure the Agent has access to these sources:

The types of context an AI Agent might need to manage include:

• **Instructions:** These are like the Agent's "rules" – prompts, system messages, few-shot examples (showing the AI how to do something), and descriptions of 工具s it can use. This is where the focus of prompt engineering combines with context engineering.

• **Knowledge:** This covers facts, information retrieved from databases, or long-term memories the Agent has accumulated. This includes integrating a Retrieval Augmented Generation (RAG) system if an Agent needs access to different knowledge stores and databases.

• **工具s:** These are the definitions of external functions, APIs and MCP Servers that the Agent can call, along with the feedback (results) it gets from using them.

• **Conversation History:** The ongoing dialogue with a user. As time passes, these conversations become longer and more complex which means they take up space in the context window.

• **User Preferences:** Information learned about a user's likes or dislikes over time. These could be stored and called upon when making key decisions to help the user.

## Strategies for Effective 上下文工程

### Planning Strategies

[![上下文工程 Best Practices](./images/best-practices.png)](https://youtu.be/F5zqRV7gEag)

Good context engineering starts with good planning. Here is an approach that will help you start to think about how to apply the concept of context engineering:

1. **Define Clear Results** - The results of the tasks that AI Agent will be assigned should be clearly defined. Answer the question - "What will the world look like when the AI Agent is done with its task?" In other words, what change, information, or response should the user have after interacting with the AI Agent.
2. **Map the Context** - Once you have defined the results of the AI Agent, you need to answer the question of "What information does the AI Agent need in order to complete this task?". This way you can start to map the context of where that information can be located.
3. **Create Context Pipelines** - Now that you know where the information is, you need to answer the question "How will the Agent get this information?". This can be done in a variety of ways including RAG, use of MCP servers and other 工具s.

### Practical Strategies

Planning is important but once the information starts to flow into our Agent's context window, we need to have practical strategies to manage it:

#### Managing Context

While some information will be added to the context window automatically, context engineering is about taking a more active role of this information which can be done by a few strategies:

 1. **Agent Scratchpad**
 This allows for an AI Agent to takes notes of relevant information about the current tasks and user interactions during a single session. This should exist outside of the context window in a file or runtime object that the Agent can later retrieve during this session if needed.

 2. **Memories**
 Scratchpads are good for managing information outside of the context window of a single session. Memories enable Agent to store and retrieve relevant information across multiple sessions. This could include summaries, user preferences and feedback for improvements in the future.

 3. **Compressing Context**
  Once the context window grows and is nearing its limit, techniques such as summarization and trimming can be used. This includes either keeping only the most relevant information or removing older messages.
  
 4. **多 Agent 系统 Systems**
  Developing multi-Agent system is a form of context engineering because each Agent has its own context window. How that context is shared and passed to different Agent is another thing to plan out when building these systems.
  
 5. **Sandbox Environments**
  If an Agent needs to run some code or process large amounts of information in a document, this can take a large amount of tokens to process the results. Instead of having this all stored in the context window, the Agent can use a sandbox environment that is able to run this code and only read the results and other relevant information.
  
 6. **Runtime State Objects**
   This is done by creating containers of information to manage situations when the Agent needs to have access to certain information. For a complex task, this would enable an Agent to store the results of each subtask step by step, allowing the context to remain connected only to that specific subtask.
  
### Example of 上下文工程

Let's say we want an AI Agent to **"Book me a trip to Paris."**

• A simple  Agent using only prompt engineering might just respond: **"Okay, when would you like to go to Paris?**". It only processed your direct question at the time that the user asked.

• An Agent using  the context engineering strategies covered would do much more. Before even responding, its system might:

  ◦ **Check your calendar** for available dates (retrieving real-time data).

 ◦ **Recall past travel preferences** (from long-term 记忆) like your preferred airline, budget, or whether you prefer direct flights.

 ◦ **Identify available 工具s** for flight and hotel booking.

- Then, an example response could be:  "Hey [Your Name]! I see you're free the first week of October. Shall I look for direct flights to Paris on [Preferred Airline] within your usual budget of [Budget]?". This richer, context-aware response demonstrates the power of context engineering.

## Common Context Failures

### Context Poisoning

**What it is:** When a hallucination (false information generated by the 大型语言模型) or an error enters the context and is repeatedly referenced, causing the Agent to pursue impossible goals or develop nonsense strategies.

**What to do:** Implement **context validation** and **quarantine**. Validate information before it's added to long-term 记忆. If potential poisoning is detected, start fresh context threads to prevent the bad information from spreading.

**Travel Booking Example:** Your Agent hallucinates a **direct flight from a small local airport to a distant international city** that doesn't actually offer international flights. This non-existent flight detail gets saved into the context. Later, when you ask the Agent to book, it keeps trying to find tickets for this impossible route, leading to repeated errors.

**Solution:** Implement a step that **validates flight existence and routes with a real-time API** _before_ adding the flight detail to the Agent's working context. If the validation fails, the erroneous information is "quarantined" and not used further.

### Context Distraction

**What it is:** When the context becomes so large that the model focuses too much on the accumulated history instead of using what it learned during training, leading to repetitive or unhelpful actions. Models may begin making mistakes even before the context window is full.

**What to do:** Use **context summarization**. Periodically compress accumulated information into shorter summaries, keeping important details while removing redundant history. This helps "reset" the focus.

**Travel Booking Example:** You've been discussing various dream travel destinations for a long time, including a detailed recounting of your backpacking trip from two years ago. When you finally ask to **"find me a cheap flight for** **next month****,"** the Agent gets bogged down in the old, irrelevant details and keeps asking about your backpacking gear or past itineraries, neglecting your current request.

**Solution:** After a certain number of turns or when the context grows too large, the Agent should **summarize the most recent and relevant parts of the conversation** – focusing on your current travel dates and destination – and use that condensed summary for the next 大型语言模型 call, discarding the less relevant historical chat.

### Context Confusion

**What it is:** When unnecessary context, often in the form of too many available 工具s, causes the model to generate bad responses or call irrelevant 工具s. Smaller models are especially prone to this.

**What to do:** Implement **工具 loadout management** using RAG techniques. Store 工具 descriptions in a vector database and select _only_ the most relevant 工具s for each specific task. Research shows limiting 工具 selections to fewer than 30.

**Travel Booking Example:** Your Agent has access to dozens of 工具s: `book_flight`, `book_hotel`, `rent_car`, `find_tours`, `currency_converter`, `weather_forecast`, `restaurant_reservations`, etc. You ask, **"What's the best way to get around Paris?"** Due to the sheer number of 工具s, the Agent gets confused and attempts to call `book_flight` _within_ Paris, or `rent_car` even though you prefer public transport, because the 工具 descriptions might overlap or it simply can't discern the best one.

**Solution:** Use **RAG over 工具 descriptions**. When you ask about getting around Paris, the system dynamically retrieves _only_ the most relevant 工具s like `rent_car` or `public_transport_info` based on your query, presenting a focused "loadout" of 工具s to the 大型语言模型.

### Context Clash

**What it is:** When conflicting information exists within the context, leading to inconsistent reasoning or bad final responses. This often happens when information arrives in stages, and early, incorrect assumptions remain in the context.

**What to do:** Use **context pruning** and **offloading**. Pruning means removing outdated or conflicting information as new details arrive. Offloading gives the model a separate "scratchpad" workspace to process information without cluttering the main context.

**Travel Booking Example:** You initially tell your Agent, **"I want to fly economy class."** Later in the conversation, you change your mind and say, **"Actually, for this trip, let's go business class."** If both instructions remain in the context, the Agent might receive conflicting search results or get confused about which preference to prioritize.

**Solution:** Implement **context pruning**. When a new instruction contradicts an old one, the older instruction is removed or explicitly overridden in the context. Alternatively, the Agent can use a **scratchpad** to reconcile conflicting preferences before deciding, ensuring only the final, consistent instruction guides its actions.

## Got More Questions About 上下文工程?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.
