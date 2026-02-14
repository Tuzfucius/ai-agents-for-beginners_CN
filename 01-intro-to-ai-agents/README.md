
[![Intro to AI Agent](./images/lesson-1-thumbnail.png)](https://youtu.be/3zgm60bXmQk?si=QA4CW2-cmul5kk3D)

> _(Click the image above to view video of this lesson)_


# AI Agent 入门 and Agent Use Cases

Welcome to the "AI Agent for Beginners" course! This course provides fundamental knowledge and applied samples for building AI Agent.

Join the <a href="https://discord.gg/kzRShWzttr" target="_blank">Azure AI Discord Community</a> to meet other learners and AI Agent Builders and ask any questions you have about this course.

To start this course, we begin by getting a better understanding of what AI Agent are and how we can use them in the applications and workflows we build.

## 简介

本节课涵盖:

- What are AI Agent and what are the different types of Agent?
- What use cases are best for AI Agent and how can they help us?
- What are some of the basic building blocks when designing Agentic Solutions?

## 学习目标
完成本节课后, you should be able to:

- Understand AI Agent concepts and how they differ from other AI solutions.
- Apply AI Agent most efficiently.
- Design Agentic solutions productively for both users and customers.

## Defining AI Agent and Types of AI Agent

### 什么是 are AI Agent?

AI Agent are **systems** that enable **Large Language Models(大型语言模型s)** to **perform actions** by extending their capabilities by giving 大型语言模型s **access to 工具s** and **knowledge**.

Let's break this definition into smaller parts:

- **System** - It's important to think about Agent not as just a single component but as a system of many components. At the basic level, the components of an AI Agent are:
  - **Environment** - The defined space where the AI Agent is operating. For example, if we had a travel booking AI Agent, the environment could be the travel booking system that the AI Agent uses to complete tasks.
  - **Sensors** - Environments have information and provide feedback. AI Agent use sensors to gather and interpret this information about the current state of the environment. In the Travel Booking Agent example, the travel booking system can provide information such as hotel availability or flight prices.
  - **Actuators** - Once the AI Agent receives the current state of the environment, for the current task the Agent determines what action to perform to change the environment. For the travel booking Agent, it might be to book an available room for the user.

![What Are AI Agent?](./images/what-are-ai-Agent.png)

**Large Language Models** - The concept of Agent existed before the creation of 大型语言模型s. The advantage of building AI Agent with 大型语言模型s is their ability to interpret human language and data. This ability enables 大型语言模型s to interpret environmental information and define a plan to change the environment.

**Perform Actions** - Outside of AI Agent systems, 大型语言模型s are limited to situations where the action is generating content or information based on a user's prompt. Inside AI Agent systems, 大型语言模型s can accomplish tasks by interpreting the user's request and using 工具s that are available in their environment.

**Access To 工具s** - What 工具s the 大型语言模型 has access to is defined by 1) the environment it's operating in and 2) the developer of the AI Agent. For our travel Agent example, the Agent's 工具s are limited by the operations available in the booking system, and/or the developer can limit the Agent's 工具 access to flights.

**记忆+Knowledge** - 记忆 can be short-term in the context of the conversation between the user and the Agent. Long-term, outside of the information provided by the environment, AI Agent can also retrieve knowledge from other systems, services, 工具s, and even other Agent. In the travel Agent example, this knowledge could be the information on the user's travel preferences located in a customer database.

### The different types of Agent

Now that we have a general definition of AI Agent, let us look at some specific Agent types and how they would be applied to a travel booking AI Agent.

| **Agent Type**                | **Description**                                                                                                                       | **Example**                                                                                                                                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Simple Reflex Agent**      | Perform immediate actions based on predefined rules.                                                                                  | Travel Agent interprets the context of the email and forwards travel complaints to customer service.                                                                                                                          |
| **Model-Based Reflex Agent** | Perform actions based on a model of the world and changes to that model.                                                              | Travel Agent prioritizes routes with significant price changes based on access to historical pricing data.                                                                                                             |
| **Goal-Based Agent**         | Create plans to achieve specific goals by interpreting the goal and determining actions to reach it.                                  | Travel Agent books a journey by determining necessary travel arrangements (car, public transit, flights) from the current location to the destination.                                                                                |
| **Utility-Based Agent**      | Consider preferences and weigh tradeoffs numerically to determine how to achieve goals.                                               | Travel Agent maximizes utility by weighing convenience vs. cost when booking travel.                                                                                                                                          |
| **Learning Agent**           | Improve over time by responding to feedback and adjusting actions accordingly.                                                        | Travel Agent improves by using customer feedback from post-trip surveys to make adjustments to future bookings.                                                                                                               |
| **Hierarchical Agent**       | Feature multiple Agent in a tiered system, with higher-level Agent breaking tasks into subtasks for lower-level Agent to complete. | Travel Agent cancels a trip by dividing the task into subtasks (for example, canceling specific bookings) and having lower-level Agent complete them, reporting back to the higher-level Agent.                                     |
| **多 Agent 系统 Systems (MAS)** | Agent complete tasks independently, either cooperatively or competitively.                                                           | Cooperative: Multiple Agent book specific travel services such as hotels, flights, and entertainment. Competitive: Multiple Agent manage and compete over a shared hotel booking calendar to book customers into the hotel. |

## When to Use AI Agent

In the earlier section, we used the Travel Agent use-case to explain how the different types of Agent can be used in different scenarios of travel booking. We will continue to use this application throughout the course.

Let's look at the types of use cases that AI Agent are best used for:

![When to use AI Agent?](./images/when-to-use-ai-Agent.png)


- **Open-Ended Problems** - allowing the 大型语言模型 to determine needed steps to complete a task because it can't always be hardcoded into a workflow.
- **Multi-Step Processes** - tasks that require a level of complexity in which the AI Agent needs to use 工具s or information over multiple turns instead of single shot retrieval.  
- **Improvement Over Time** - tasks where the Agent can improve over time by receiving feedback from either its environment or users in order to provide better utility.

We cover more considerations of using AI Agent in the Building Trustworthy AI Agent lesson.

## Basics of Agentic Solutions

### Agent Development

The first step in designing an AI Agent system is to define the 工具s, actions, and behaviors. In this course, we focus on using the **Azure AI Agent Service** to define our Agent. It offers features like:

- Selection of Open Models such as OpenAI, Mistral, and Llama
- Use of Licensed Data through providers such as Tripadvisor
- Use of standardized OpenAPI 3.0 工具s

### Agentic 模式s

Communication with 大型语言模型s is through prompts. Given the semi-autonomous nature of AI Agent, it isn't always possible or required to manually reprompt the 大型语言模型 after a change in the environment. We use **Agentic 模式s** that allow us to prompt the 大型语言模型 over multiple steps in a more scalable way.

This course is divided into some of the current popular Agentic 模式s.

### Agentic 框架s

Agentic 框架s allow developers to implement Agentic 模式s through code. These 框架s offer templates, plugins, and 工具s for better AI Agent collaboration. These benefits provide abilities for better observability and troubleshooting of AI Agent systems.

In this course, we will explore the research-driven AutoGen 框架 and the production-ready Agent 框架 from Semantic Kernel.

## 示例代码s

- Python: [Agent 框架](./code_samples/01-python-Agent-框架.ipynb)
- .NET: [Agent 框架](./code_samples/01-dotnet-Agent-框架.md)

## Got More Questions about AI Agent?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.

## 上一课

[课程设置](../00-course-setup/README.md)

## 下一课

[探索 Agentic 框架](../02-explore-Agentic-框架s/README.md)
