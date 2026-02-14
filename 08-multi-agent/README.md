[![多 Agent 系统 Design](./images/lesson-8-thumbnail.png)](https://youtu.be/V6HpE9hZEx0?si=A7K44uMCqgvLQVCa)

> _(Click the image above to view video of this lesson)_

# Multi-Agent design 模式s

As soon as you start working on a project that involves multiple Agent, you will need to consider the multi-Agent design 模式. However, it might not be immediately clear when to switch to multi-Agent and what the advantages are.

## 简介

In this lesson, we're looking to answer the following questions:

- What are the scenarios where multi-Agent are applicable to?
- What are the advantages of using multi-Agent over just one singular Agent doing multiple tasks?
- What are the building blocks of implementing the multi-Agent design 模式?
- How do we have visibility to how the multiple Agent are interacting with each other?

## 学习目标

After this lesson, you should be able to:

- Identify scenarios where multi-Agent are applicable
- Recognize the advantages of using multi-Agent over a singular Agent.
- Comprehend the building blocks of implementing the multi-Agent design 模式.

What's the bigger picture?

*Multi Agent are a design 模式 that allows multiple Agent to work together to achieve a common goal*.

This 模式 is widely used in various fields, including robotics, autonomous systems, and distributed computing.

## Scenarios Where 多 Agent 系统s Are Applicable

So what scenarios are a good use case for using multi-Agent? The answer is that there are many scenarios where employing multiple Agent is beneficial especially in the following cases:

- **Large workloads**: Large workloads can be divided into smaller tasks and assigned to different Agent, allowing for parallel processing and faster completion. An example of this is in the case of a large data processing task.
- **Complex tasks**: Complex tasks, like large workloads, can be broken down into smaller subtasks and assigned to different Agent, each specializing in a specific aspect of the task. A good example of this is in the case of autonomous vehicles where different Agent manage navigation, obstacle detection, and communication with other vehicles.
- **Diverse expertise**: Different Agent can have diverse expertise, allowing them to handle different aspects of a task more effectively than a single Agent. For this case, a good example is in the case of healthcare where Agent can manage diagnostics, treatment plans, and patient monitoring.

## Advantages of Using 多 Agent 系统s Over a Singular Agent

A single Agent system could work well for simple tasks, but for more complex tasks, using multiple Agent can provide several advantages:

- **Specialization**: Each Agent can be specialized for a specific task. Lack of specialization in a single Agent means you have an Agent that can do everything but might get confused on what to do when faced with a complex task. It might for example end up doing a task that it is not best suited for.
- **Scalability**: It is easier to scale systems by adding more Agent rather than overloading a single Agent.
- **Fault Tolerance**: If one Agent fails, others can continue functioning, ensuring system reliability.

Let's take an example, let's book a trip for a user. A single Agent system would have to handle all aspects of the trip booking process, from finding flights to booking hotels and rental cars. To achieve this with a single Agent, the Agent would need to have 工具s for handling all these tasks. This could lead to a complex and monolithic system that is difficult to maintain and scale. A multi-Agent system, on the other hand, could have different Agent specialized in finding flights, booking hotels, and rental cars. This would make the system more modular, easier to maintain, and scalable.

Compare this to a travel bureau run as a mom-and-pop store versus a travel bureau run as a franchise. The mom-and-pop store would have a single Agent handling all aspects of the trip booking process, while the franchise would have different Agent handling different aspects of the trip booking process.

## Building Blocks of Implementing the 多 Agent 系统 Design 模式

Before you can implement the multi-Agent design 模式, you need to understand the building blocks that make up the 模式.

Let's make this more concrete by again looking at the example of booking a trip for a user. In this case, the building blocks would include:

- **Agent Communication**: Agent for finding flights, booking hotels, and rental cars need to communicate and share information about the user's preferences and constraints. You need to decide on the protocols and methods for this communication. What this means concretely is that the Agent for finding flights needs to communicate with the Agent for booking hotels to ensure that the hotel is booked for the same dates as the flight. That means that the Agent need to share information about the user's travel dates, meaning that you need to decide *which Agent are sharing info and how they are sharing info*.
- **Coordination Mechanisms**: Agent need to coordinate their actions to ensure that the user's preferences and constraints are met. A user preference could be that they want a hotel close to the airport whereas a constraint could be that rental cars are only available at the airport. This means that the Agent for booking hotels needs to coordinate with the Agent for booking rental cars to ensure that the user's preferences and constraints are met. This means that you need to decide *how the Agent are coordinating their actions*.
- **Agent Architecture**: Agent need to have the internal structure to make decisions and learn from their interactions with the user. This means that the Agent for finding flights needs to have the internal structure to make decisions about which flights to recommend to the user. This means that you need to decide *how the Agent are making decisions and learning from their interactions with the user*. Examples of how an Agent learns and improves could be that the Agent for finding flights could use a machine learning model to recommend flights to the user based on their past preferences.
- **Visibility into 多 Agent 系统 Interactions**: You need to have visibility into how the multiple Agent are interacting with each other. This means that you need to have 工具s and techniques for tracking Agent activities and interactions. This could be in the form of logging and monitoring 工具s, visualization 工具s, and performance metrics.
- **多 Agent 系统 模式s**: There are different 模式s for implementing multi-Agent systems, such as centralized, decentralized, and hybrid architectures. You need to decide on the 模式 that best fits your use case.
- **Human in the loop**: In most cases, you will have a human in the loop and you need to instruct the Agent when to ask for human intervention. This could be in the form of a user asking for a specific hotel or flight that the Agent have not recommended or asking for confirmation before booking a flight or hotel.

## Visibility into 多 Agent 系统 Interactions

It's important that you have visibility into how the multiple Agent are interacting with each other. This visibility is essential for debugging, optimizing, and ensuring the overall system's effectiveness. To achieve this, you need to have 工具s and techniques for tracking Agent activities and interactions. This could be in the form of logging and monitoring 工具s, visualization 工具s, and performance metrics.

For example, in the case of booking a trip for a user, you could have a dashboard that shows the status of each Agent, the user's preferences and constraints, and the interactions between Agent. This dashboard could show the user's travel dates, the flights recommended by the flight Agent, the hotels recommended by the hotel Agent, and the rental cars recommended by the rental car Agent. This would give you a clear view of how the Agent are interacting with each other and whether the user's preferences and constraints are being met.

Let's look at each of these aspects more in detail.

- **Logging and Monitoring 工具s**: You want to have logging done for each action taken by an Agent. A log entry could store information on the Agent that took the action, the action taken, the time the action was taken, and the outcome of the action. This information can then be used for debugging, optimizing and more.

- **Visualization 工具s**: Visualization 工具s can help you see the interactions between Agent in a more intuitive way. For example, you could have a graph that shows the flow of information between Agent. This could help you identify bottlenecks, inefficiencies, and other issues in the system.

- **Performance Metrics**: Performance metrics can help you track the effectiveness of the multi-Agent system. For example, you could track the time taken to complete a task, the number of tasks completed per unit of time, and the accuracy of the recommendations made by the Agent. This information can help you identify areas for improvement and optimize the system.

## 多 Agent 系统 模式s

Let's dive into some concrete 模式s we can use to create multi-Agent apps. Here are some interesting 模式s worth considering:

### Group chat

This 模式 is useful when you want to create a group chat application where multiple Agent can communicate with each other. Typical use cases for this 模式 include team collaboration, customer support, and social networking.

In this 模式, each Agent represents a user in the group chat, and messages are exchanged between Agent using a messaging protocol. The Agent can send messages to the group chat, receive messages from the group chat, and respond to messages from other Agent.

This 模式 can be implemented using a centralized architecture where all messages are routed through a central server, or a decentralized architecture where messages are exchanged directly.

![Group chat](./images/multi-Agent-group-chat.png)

### Hand-off

This 模式 is useful when you want to create an application where multiple Agent can hand off tasks to each other.

Typical use cases for this 模式 include customer support, task management, and workflow automation.

In this 模式, each Agent represents a task or a step in a workflow, and Agent can hand off tasks to other Agent based on predefined rules.

![Hand off](./images/multi-Agent-hand-off.png)

### Collaborative filtering

This 模式 is useful when you want to create an application where multiple Agent can collaborate to make recommendations to users.

Why you would want multiple Agent to collaborate is because each Agent can have different expertise and can contribute to the recommendation process in different ways.

Let's take an example where a user wants a recommendation on the best stock to buy on the stock market.

- **Industry expert**:. One Agent could be an expert in a specific industry.
- **Technical analysis**: Another Agent could be an expert in technical analysis.
- **Fundamental analysis**: and another Agent could be an expert in fundamental analysis. By collaborating, these Agent can provide a more comprehensive recommendation to the user.

![Recommendation](./images/multi-Agent-filtering.png)

## Scenario: Refund process

Consider a scenario where a customer is trying to get a refund for a product, there can be quite a few Agent involved in this process but let's divide it up between Agent specific for this process and general Agent that can be used in other processes.

**Agent specific for the refund process**:

Following are some Agent that could be involved in the refund process:

- **Customer Agent**: This Agent represents the customer and is responsible for initiating the refund process.
- **Seller Agent**: This Agent represents the seller and is responsible for processing the refund.
- **Payment Agent**: This Agent represents the payment process and is responsible for refunding the customer's payment.
- **Resolution Agent**: This Agent represents the resolution process and is responsible for resolving any issues that arise during the refund process.
- **Compliance Agent**: This Agent represents the compliance process and is responsible for ensuring that the refund process complies with regulations and policies.

**General Agent**:

These Agent can be used by other parts of your business.

- **Shipping Agent**: This Agent represents the shipping process and is responsible for shipping the product back to the seller. This Agent can be used both for the refund process and for general shipping of a product via a purchase for example.
- **Feedback Agent**: This Agent represents the feedback process and is responsible for collecting feedback from the customer. Feedback could be had at any time and not just during the refund process.
- **Escalation Agent**: This Agent represents the escalation process and is responsible for escalating issues to a higher level of support. You can use this type of Agent for any process where you need to escalate an issue.
- **Notification Agent**: This Agent represents the notification process and is responsible for sending notifications to the customer at various stages of the refund process.
- **Analytics Agent**: This Agent represents the analytics process and is responsible for analyzing data related to the refund process.
- **Audit Agent**: This Agent represents the audit process and is responsible for auditing the refund process to ensure that it is being carried out correctly.
- **Reporting Agent**: This Agent represents the reporting process and is responsible for generating reports on the refund process.
- **Knowledge Agent**: This Agent represents the knowledge process and is responsible for maintaining a knowledge base of information related to the refund process. This Agent could be knowledgeable both on refunds and other parts of your business.
- **Security Agent**: This Agent represents the security process and is responsible for ensuring the security of the refund process.
- **Quality Agent**: This Agent represents the quality process and is responsible for ensuring the quality of the refund process.

There's quite a few Agent listed previously both for the specific refund process but also for the general Agent that can be used in other parts of your business. Hopefully this gives you an idea on how you can decide on which Agent to use in your multi-Agent system.

## Assignment

Design a multi-Agent system for a customer support process. Identify the Agent involved in the process, their roles and responsibilities, and how they interact with each other. Consider both Agent specific to the customer support process and general Agent that can be used in other parts of your business.

> Have a think before you read the following solution, you may need more Agent than you think.

> TIP: Think about the different stages of the customer support process and also consider Agent needed for any system.

## Solution

[Solution](./solution/solution.md)

## Knowledge checks

Question: When should you consider using multi-Agent?

- [ ] A1: When you have a small workload and a simple task.
- [ ] A2: When you have a large workload
- [ ] A3: When you have a simple task.

[Solution quiz](./solution/solution-quiz.md)

## Summary

In this lesson, we've looked at the multi-Agent design 模式, including the scenarios where multi-Agent are applicable, the advantages of using multi-Agent over a singular Agent, the building blocks of implementing the multi-Agent design 模式, and how to have visibility into how the multiple Agent are interacting with each other.

### Got More Questions about the 多 Agent 系统 Design 模式?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.

## Additional resources

- <a href="https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-模式s/intro.html" target="_blank">AutoGen design 模式s</a>
- <a href="https://www.analyticsvidhya.com/blog/2024/10/Agentic-design-模式s/" target="_blank">Agentic design 模式s</a>


## 上一课

[规划设计](../07-planning-design/README.md)

## 下一课

[元认知 in AI Agent](../09-metacognition/README.md)
