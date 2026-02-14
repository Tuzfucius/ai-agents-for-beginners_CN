# 生产环境中的 AI Agent: Observability & Evaluation

[![生产环境中的 AI Agent](./images/lesson-10-thumbnail.png)](https://youtu.be/l4TP6IyJxmQ?si=reGOyeqjxFevyDq9)

As AI Agent move from experimental prototypes to real-world applications, the ability to understand their behavior, monitor their performance, and systematically evaluate their outputs becomes important.

## 学习目标

完成本节课后, you will know how to/understand:
- Core concepts of Agent observability and evaluation
- Techniques for improving the performance, costs, and effectiveness of Agent
- What and how to evaluate your AI Agent systematically
- How to control costs when deploying AI Agent to production
- How to instrument Agent built with AutoGen

The goal is to equip you with the knowledge to transform your "black box" Agent into transparent, manageable, and dependable systems.

_**Note:** It is important to deploy AI Agent that are safe and trustworthy. Check out the [Building Trustworthy AI Agent](./06-building-trustworthy-Agent/README.md) lesson as well._

## Traces and Spans

Observability 工具s such as [Langfuse](https://langfuse.com/) or [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry) usually represent Agent runs as traces and spans.

- **Trace** represents a complete Agent task from start to finish (like handling a user query).
- **Spans** are individual steps within the trace (like calling a language model or retrieving data).

![Trace tree in Langfuse](https://langfuse.com/images/cookbook/example-autogen-evaluation/trace-tree.png)

Without observability, an AI Agent can feel like a "black box" - its internal state and reasoning are opaque, making it difficult to diagnose issues or optimize performance. With observability, Agent become "glass boxes," offering transparency that is vital for building trust and ensuring they operate as intended. 

## Why Observability Matters in Production Environments

Transitioning AI Agent to production environments introduces a new set of challenges and requirements. Observability is no longer a "nice-to-have" but a critical capability:

*   **Debugging and Root-Cause Analysis**: When an Agent fails or produces an unexpected output, observability 工具s provide the traces needed to pinpoint the source of the error. This is especially important in complex Agent that might involve multiple 大型语言模型 calls, 工具 interactions, and conditional logic.
*   **Latency and Cost Management**: AI Agent often rely on 大型语言模型s and other external APIs that are billed per token or per call. Observability allows for precise tracking of these calls, helping to identify operations that are excessively slow or expensive. This enables teams to optimize prompts, select more efficient models, or redesign workflows to manage operational costs and ensure a good user experience.
*   **Trust, Safety, and Compliance**: In many applications, it's important to ensure that Agent behave safely and ethically. Observability provides an audit trail of Agent actions and decisions. This can be used to detect and mitigate issues like prompt injection, the generation of harmful content, or the mishandling of personally identifiable information (PII). For example, you can review traces to understand why an Agent provided a certain response or used a specific 工具.
*   **Continuous Improvement Loops**: Observability data is the foundation of an iterative development process. By monitoring how Agent perform in the real world, teams can identify areas for improvement, gather data for fine-tuning models, and validate the impact of changes. This creates a feedback loop where production insights from online evaluation inform offline experimentation and refinement, leading to progressively better Agent performance.

## Key Metrics to Track

To monitor and understand Agent behavior, a range of metrics and signals should be tracked. While the specific metrics might vary based on the Agent's purpose, some are universally important.

Here are some of the most common metrics that observability 工具s monitor:

**Latency:** How quickly does the Agent respond? Long waiting times negatively impact user experience. You should measure latency for tasks and individual steps by tracing Agent runs. For example, an Agent that takes 20 seconds for all model calls could be accelerated by using a faster model or by running model calls in parallel.

**Costs:** What’s the expense per Agent run? AI Agent rely on 大型语言模型 calls billed per token or external APIs. Frequent 工具 usage or multiple prompts can rapidly increase costs. For instance, if an Agent calls an 大型语言模型 five times for marginal quality improvement, you must assess if the cost is justified or if you could reduce the number of calls or use a cheaper model. Real-time monitoring can also help identify unexpected spikes (e.g., bugs causing excessive API loops).

**Request Errors:** How many requests did the Agent fail? This can include API errors or failed 工具 calls. To make your Agent more robust against these in production, you can then set up fallbacks or retries. E.g. if 大型语言模型 provider A is down, you switch to 大型语言模型 provider B as backup.

**User Feedback:** Implementing direct user evaluations provide valuable insights. This can include explicit ratings (👍thumbs-up/👎down, ⭐1-5 stars) or textual comments. Consistent negative feedback should alert you as this is a sign that the Agent is not working as expected. 

**Implicit User Feedback:** User behaviors provide indirect feedback even without explicit ratings. This can include immediate question rephrasing, repeated queries or clicking a retry button. E.g. if you see that users repeatedly ask the same question, this is a sign that the Agent is not working as expected.

**Accuracy:** How frequently does the Agent produce correct or desirable outputs? Accuracy definitions vary (e.g., problem-solving correctness, information retrieval accuracy, user satisfaction). The first step is to define what success looks like for your Agent. You can track accuracy via automated checks, evaluation scores, or task completion labels. For example, marking traces as "succeeded" or "failed". 

**Automated Evaluation Metrics:** You can also set up automated evals. For instance, you can use an 大型语言模型 to score the output of the Agent e.g. if it is helpful, accurate, or not. There are also several open source libraries that help you to score different aspects of the Agent. E.g. [RAGAS](https://docs.ragas.io/) for RAG Agent or [大型语言模型 Guard](https://llm-guard.com/) to detect harmful language or prompt injection. 

In practice, a combination of these metrics gives the best coverage of an AI Agent’s health. In this chapters [example notebook](./code_samples/10_autogen_evaluation.ipynb), we'll show you how these metrics looks in real examples but first, we'll learn how a typical evaluation workflow looks like.

## Instrument your Agent

To gather tracing data, you’ll need to instrument your code. The goal is to instrument the Agent code to emit traces and metrics that can be captured, processed, and visualized by an observability platform.

**OpenTelemetry (OTel):** [OpenTelemetry](https://opentelemetry.io/) has emerged as an industry standard for 大型语言模型 observability. It provides a set of APIs, SDKs, and 工具s for generating, collecting, and exporting telemetry data. 

There are many instrumentation libraries that wrap existing Agent 框架s and make it easy to export OpenTelemetry spans to an observability 工具. Below is an example on instrumenting an AutoGen Agent with the [OpenLit instrumentation library](https://github.com/openlit/openlit):

```python
import openlit

openlit.init(tracer = langfuse._otel_tracer, disable_batch = True)
```

The [example notebook](./code_samples/10_autogen_evaluation.ipynb) in this chapter will demonstrate how to instrument your AutoGen Agent.

**Manual Span Creation:** While instrumentation libraries provides a good baseline, there are often cases where more detailed or custom information is needed. You can manually create spans to add custom application logic. More importantly, they can enrich automatically or manually created spans with custom attributes (also known as tags or metadata). These attributes can include business-specific data, intermediate computations, or any context that might be useful for debugging or analysis, such as `user_id`, `session_id`, or `model_version`.

Example on creating traces and spans manually with the [Langfuse Python SDK](https://langfuse.com/docs/sdk/python/sdk-v3): 

```python
from langfuse import get_client
 
langfuse = get_client()
 
span = langfuse.start_span(name="my-span")
 
span.end()
```

## Agent Evaluation

Observability gives us metrics, but evaluation is the process of analyzing that data (and performing tests) to determine how well an AI Agent is performing and how it can be improved. In other words, once you have those traces and metrics, how do you use them to judge the Agent and make decisions? 

Regular evaluation is important because AI Agent are often non-deterministic and can evolve (through updates or drifting model behavior) – without evaluation, you wouldn’t know if your “smart Agent” is actually doing its job well or if it’s regressed.

There are two categories of evaluations for AI Agent: **online evaluation** and **offline evaluation**. Both are valuable, and they complement each other. We usually begin with offline evaluation, as this is the minimum necessary step before deploying any Agent.

### Offline Evaluation

![Dataset items in Langfuse](https://langfuse.com/images/cookbook/example-autogen-evaluation/example-dataset.png)

This involves evaluating the Agent in a controlled setting, typically using test datasets, not live user queries. You use curated datasets where you know what the expected output or correct behavior is, and then run your Agent on those. 

For instance, if you built a math word-problem Agent, you might have a [test dataset](https://huggingface.co/datasets/gsm8k) of 100 problems with known answers. Offline evaluation is often done during development (and can be part of CI/CD pipelines) to check improvements or guard against regressions. The benefit is that it’s **repeatable and you can get clear accuracy metrics since you have ground truth**. You might also simulate user queries and measure the Agent’s responses against ideal answers or use automated metrics as described above. 

The key challenge with offline eval is ensuring your test dataset is comprehensive and stays relevant – the Agent might perform well on a fixed test set but encounter very different queries in production. Therefore, you should keep test sets updated with new edge cases and examples that reflect real-world scenarios​. A mix of small “smoke test” cases and larger evaluation sets is useful: small sets for quick checks and larger ones for broader performance metrics​.

### Online Evaluation 

![Observability metrics overview](https://langfuse.com/images/cookbook/example-autogen-evaluation/dashboard.png)

This refers to evaluating the Agent in a live, real-world environment, i.e. during actual usage in production. Online evaluation involves monitoring the Agent’s performance on real user interactions and analyzing outcomes continuously. 

For example, you might track success rates, user satisfaction scores, or other metrics on live traffic. The advantage of online evaluation is that it **captures things you might not anticipate in a lab setting** – you can observe model drift over time (if the Agent’s effectiveness degrades as input 模式s shift) and catch unexpected queries or situations that weren’t in your test data​. It provides a true picture of how the Agent behaves in the wild. 

Online evaluation often involves collecting implicit and explicit user feedback, as discussed, and possibly running shadow tests or A/B tests (where a new version of the Agent runs in parallel to compare against the old). The challenge is that it can be tricky to get reliable labels or scores for live interactions – you might rely on user feedback or downstream metrics (like did the user click the result). 

### Combining the two

Online and offline evaluations are not mutually exclusive; they are highly complementary. Insights from online monitoring (e.g., new types of user queries where the Agent performs poorly) can be used to augment and improve offline test datasets. Conversely, Agent that perform well in offline tests can then be more confidently deployed and monitored online. 

In fact, many teams adopt a loop: 

_evaluate offline -> deploy -> monitor online -> collect new failure cases -> add to offline dataset -> refine Agent -> repeat_.

## Common Issues

As you deploy AI Agent to production, you may encounter various challenges. Here are some common issues and their potential solutions:

| **Issue**    | **Potential Solution**   |
| ------------- | ------------------ |
| AI Agent not performing tasks consistently | - Refine the prompt given to the AI Agent; be clear on objectives.<br>- Identify where dividing the tasks into subtasks and handling them by multiple Agent can help. |
| AI Agent running into continuous loops  | - Ensure you have clear termination terms and conditions so the Agent knows when to stop the process.<br>- For complex tasks that require reasoning and planning, use a larger model that is specialized for reasoning tasks. |
| AI Agent 工具 calls are not performing well   | - Test and validate the 工具's output outside of the Agent system.<br>- Refine the defined parameters, prompts, and naming of 工具s.  |
| 多 Agent 系统 system not performing consistently | - Refine prompts given to each Agent to ensure they are specific and distinct from one another.<br>- Build a hierarchical system using a "routing" or controller Agent to determine which Agent is the correct one. |

Many of these issues can be identified more effectively with observability in place. The traces and metrics we discussed earlier help pinpoint exactly where in the Agent workflow problems occur, making debugging and optimization much more efficient.

## Managing Costs

Here are some strategies to manage the costs of deploying AI Agent to production:

**Using Smaller Models:** Small Language Models (SLMs) can perform well on certain Agentic use-cases and will reduce costs significantly. As mentioned earlier, building an evaluation system to determine and compare performance vs larger models is the best way to understand how well an SLM will perform on your use case. Consider using SLMs for simpler tasks like intent classification or parameter extraction, while reserving larger models for complex reasoning.

**Using a Router Model:** A similar strategy is to use a diversity of models and sizes. You can use an 大型语言模型/SLM or serverless function to route requests based on complexity to the best fit models. This will also help reduce costs while also ensuring performance on the right tasks. For example, route simple queries to smaller, faster models, and only use expensive large models for complex reasoning tasks.

**Caching Responses:** Identifying common requests and tasks and providing the responses before they go through your Agentic system is a good way to reduce the volume of similar requests. You can even implement a flow to identify how similar a request is to your cached requests using more basic AI models. This strategy can significantly reduce costs for frequently asked questions or common workflows.

## Lets see how this works in practice

In the [example notebook of this section](./code_samples/10_autogen_evaluation.ipynb), we’ll see examples of how we can use observability 工具s to monitor and evaluate our Agent.


### Got More Questions about 生产环境中的 AI Agent?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.

## 上一课

[元认知 Design 模式](../09-metacognition/README.md)

## 下一课

[Agentic Protocols](../11-Agentic-protocols/README.md)
