[![How to Design Good AI Agent](./images/lesson-4-thumbnail.png)](https://youtu.be/vieRiPRx-gI?si=cEZ8ApnT6Sus9rhn)

> _(Click the image above to view video of this lesson)_

# 工具使用 Design 模式

工具s are interesting because they allow AI Agent to have a broader range of capabilities. Instead of the Agent having a limited set of actions it can perform, by adding a 工具, the Agent can now perform a wide range of actions. In this chapter, we will look at the 工具使用 Design 模式, which describes how AI Agent can use specific 工具s to achieve their goals.

## 简介

In this lesson, we're looking to answer the following questions:

- What is the 工具 use design 模式?
- What are the use cases it can be applied to?
- What are the elements/building blocks needed to implement the design 模式?
- What are the special considerations for using the 工具使用 Design 模式 to build trustworthy AI Agent?

## 学习目标

完成本节课后, you will be able to:

- Define the 工具使用 Design 模式 and its purpose.
- Identify use cases where the 工具使用 Design 模式 is applicable.
- Understand the key elements needed to implement the design 模式.
- Recognize considerations for ensuring trustworthiness in AI Agent using this design 模式.

## 什么是 is the 工具使用 Design 模式?

The **工具使用 Design 模式** focuses on giving 大型语言模型s the ability to interact with external 工具s to achieve specific goals. 工具s are code that can be executed by an Agent to perform actions. A 工具 can be a simple function such as a calculator, or an API call to a third-party service such as stock price lookup or weather forecast. In the context of AI Agent, 工具s are designed to be executed by Agent in response to **model-generated function calls**.

## 什么是 are the use cases it can be applied to?

AI Agent can leverage 工具s to complete complex tasks, retrieve information, or make decisions. The 工具 use design 模式 is often used in scenarios requiring dynamic interaction with external systems, such as databases, web services, or code interpreters. This ability is useful for a number of different use cases including:

- **Dynamic Information Retrieval:** Agent can query external APIs or databases to fetch up-to-date data (e.g., querying a SQLite database for data analysis, fetching stock prices or weather information).
- **Code Execution and Interpretation:** Agent can execute code or scripts to solve mathematical problems, generate reports, or perform simulations.
- **Workflow Automation:** Automating repetitive or multi-step workflows by integrating 工具s like task schedulers, email services, or data pipelines.
- **Customer Support:** Agent can interact with CRM systems, ticketing platforms, or knowledge bases to resolve user queries.
- **Content Generation and Editing:** Agent can leverage 工具s like grammar checkers, text summarizers, or content safety evaluators to assist with content creation tasks.

## 什么是 are the elements/building blocks needed to implement the 工具 use design 模式?

These building blocks allow the AI Agent to perform a wide range of tasks. Let's look at the key elements needed to implement the 工具使用 Design 模式:

- **Function/工具 Schemas**: Detailed definitions of available 工具s, including function name, purpose, required parameters, and expected outputs. These schemas enable the 大型语言模型 to understand what 工具s are available and how to construct valid requests.

- **Function Execution Logic**: Governs how and when 工具s are invoked based on the user’s intent and conversation context. This may include planner modules, routing mechanisms, or conditional flows that determine 工具 usage dynamically.

- **Message Handling System**: Components that manage the conversational flow between user inputs, 大型语言模型 responses, 工具 calls, and 工具 outputs.

- **工具 Integration 框架**: Infrastructure that connects the Agent to various 工具s, whether they are simple functions or complex external services.

- **Error Handling & Validation**: Mechanisms to handle failures in 工具 execution, validate parameters, and manage unexpected responses.

- **State Management**: Tracks conversation context, previous 工具 interactions, and persistent data to ensure consistency across multi-turn interactions.

Next, let's look at Function/工具 Calling in more detail.
 
### Function/工具 Calling

Function calling is the primary way we enable Large Language Models (大型语言模型s) to interact with 工具s. You will often see 'Function' and '工具' used interchangeably because 'functions' (blocks of reusable code) are the '工具s' Agent use to carry out tasks. In order for a function's code to be invoked, an 大型语言模型 must compare the users request against the functions description. To do this a schema containing the descriptions of all the available functions is sent to the 大型语言模型. The 大型语言模型 then selects the most appropriate function for the task and returns its name and arguments. The selected function is invoked, it's response is sent back to the 大型语言模型, which uses the information to respond to the users request.

For developers to implement function calling for Agent, you will need:

1. An 大型语言模型 model that supports function calling
2. A schema containing function descriptions
3. The code for each function described

Let's use the example of getting the current time in a city to illustrate:

1. **Initialize an 大型语言模型 that supports function calling:**

    Not all models support function calling, so it's important to check that the 大型语言模型 you are using does.     <a href="https://learn.microsoft.com/azure/ai-services/openai/how-to/function-calling" target="_blank">Azure OpenAI</a> supports function calling. We can start by initiating the Azure OpenAI client. 

    ```python
    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-05-01-preview"
    )
    ```

1. **Create a Function Schema**:

    Next we will define a JSON schema that contains the function name, description of what the function does, and the names and descriptions of the function parameters.
    We will then take this schema and pass it to the client created previously, along with the users request to find the time in San Francisco. What's important to note is that a **工具 call** is what is returned, **not** the final answer to the question. As mentioned earlier, the 大型语言模型 returns the name of the function it selected for the task, and the arguments that will be passed to it.

    ```python
    # Function description for the model to read
    工具s = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]
    ```
   
    ```python
  
    # Initial user message
    messages = [{"role": "user", "content": "What's the current time in San Francisco"}] 
  
    # First API call: Ask the model to use the function
      response = client.chat.completions.create(
          model=deployment_name,
          messages=messages,
          工具s=工具s,
          工具_choice="auto",
      )
  
      # Process the model's response
      response_message = response.choices[0].message
      messages.append(response_message)
  
      print("Model's response:")  

      print(response_message)
  
    ```

    ```bash
    Model's response:
    ChatCompletionMessage(content=None, role='assistant', function_call=None, 工具_calls=[ChatCompletionMessage工具Call(id='call_pOsKdUlqvdyttYB67MOj434b', function=Function(arguments='{"location":"San Francisco"}', name='get_current_time'), type='function')])
    ```
  
1. **The function code required to carry out the task:**

    Now that the 大型语言模型 has chosen which function needs to be run the code that carries out the task needs to be implemented and executed.
    We can implement the code to get the current time in Python. We will also need to write the code to extract the name and arguments from the response_message to get the final result.

    ```python
      def get_current_time(location):
        """Get the current time for a given location"""
        print(f"get_current_time called with location: {location}")  
        location_lower = location.lower()
        
        for key, timezone in TIMEZONE_DATA.items():
            if key in location_lower:
                print(f"Timezone found for {key}")  
                current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
                return json.dumps({
                    "location": location,
                    "current_time": current_time
                })
      
        print(f"No timezone data found for {location_lower}")  
        return json.dumps({"location": location, "current_time": "unknown"})
    ```

     ```python
     # Handle function calls
      if response_message.工具_calls:
          for 工具_call in response_message.工具_calls:
              if 工具_call.function.name == "get_current_time":
     
                  function_args = json.loads(工具_call.function.arguments)
     
                  time_response = get_current_time(
                      location=function_args.get("location")
                  )
     
                  messages.append({
                      "工具_call_id": 工具_call.id,
                      "role": "工具",
                      "name": "get_current_time",
                      "content": time_response,
                  })
      else:
          print("No 工具 calls were made by the model.")  
  
      # Second API call: Get the final response from the model
      final_response = client.chat.completions.create(
          model=deployment_name,
          messages=messages,
      )
  
      return final_response.choices[0].message.content
     ```

     ```bash
      get_current_time called with location: San Francisco
      Timezone found for san francisco
      The current time in San Francisco is 09:24 AM.
     ```

Function Calling is at the heart of most, if not all Agent 工具 use design, however implementing it from scratch can sometimes be challenging.
As we learned in [Lesson 2](../02-explore-Agentic-框架s/) Agentic 框架s provide us with pre-built building blocks to implement 工具 use.
 
## 工具使用 Examples with Agentic 框架s

Here are some examples of how you can implement the 工具使用 Design 模式 using different Agentic 框架s:

### Semantic Kernel

<a href="https://learn.microsoft.com/azure/ai-services/Agent/overview" target="_blank">Semantic Kernel</a> is an open-source AI 框架 for .NET, Python, and Java developers working with Large Language Models (大型语言模型s). It simplifies the process of using function calling by automatically describing your functions and their parameters to the model through a process called <a href="https://learn.microsoft.com/semantic-kernel/concepts/ai-services/chat-completion/function-calling/?pivots=programming-language-python#1-serializing-the-functions" target="_blank">serializing</a>. It also handles the back-and-forth communication between the model and your code. Another advantage of using an Agentic 框架 like Semantic Kernel, is that it allows you to access pre-built 工具s like <a href="https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_Agent/openai_assistant/step4_assistant_工具_file_search.py" target="_blank">File Search</a> and <a href="https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_Agent/openai_assistant/step3_assistant_工具_code_interpreter.py" target="_blank">Code Interpreter</a>.

The following diagram illustrates the process of function calling with Semantic Kernel:

![function calling](./images/functioncalling-diagram.png)

In Semantic Kernel functions/工具s are called <a href="https://learn.microsoft.com/semantic-kernel/concepts/plugins/?pivots=programming-language-python" target="_blank">Plugins</a>. We can convert the `get_current_time` function we saw earlier into a plugin by turning it into a class with the function in it. We can also import the `kernel_function` decorator, which takes in the description of the function. When you then create a kernel with the GetCurrentTimePlugin, the kernel will automatically serialize the function and its parameters, creating the schema to send to the 大型语言模型 in the process.

```python
from semantic_kernel.functions import kernel_function

class GetCurrentTimePlugin:
    async def __init__(self, location):
        self.location = location

    @kernel_function(
        description="Get the current time for a given location"
    )
    def get_current_time(location: str = ""):
        ...

```

```python 
from semantic_kernel import Kernel

# Create the kernel
kernel = Kernel()

# Create the plugin
get_current_time_plugin = GetCurrentTimePlugin(location)

# Add the plugin to the kernel
kernel.add_plugin(get_current_time_plugin)
```
  
### Azure AI Agent Service

<a href="https://learn.microsoft.com/azure/ai-services/Agent/overview" target="_blank">Azure AI Agent Service</a> is a newer Agentic 框架 that is designed to empower developers to securely build, deploy, and scale high-quality, and extensible AI Agent without needing to manage the underlying compute and storage resources. It is particularly useful for enterprise applications since it is a fully managed service with enterprise grade security.

When compared to developing with the 大型语言模型 API directly, Azure AI Agent Service provides some advantages, including:

- Automatic 工具 calling – no need to parse a 工具 call, invoke the 工具, and handle the response; all of this is now done server-side
- Securely managed data – instead of managing your own conversation state, you can rely on threads to store all the information you need
- Out-of-the-box 工具s – 工具s that you can use to interact with your data sources, such as Bing, Azure AI Search, and Azure Functions.

The 工具s available in Azure AI Agent Service can be divided into two categories:

1. Knowledge 工具s:
    - <a href="https://learn.microsoft.com/azure/ai-services/Agent/how-to/工具s/bing-grounding?tabs=python&pivots=overview" target="_blank">Grounding with Bing Search</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/Agent/how-to/工具s/file-search?tabs=python&pivots=overview" target="_blank">File Search</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/Agent/how-to/工具s/azure-ai-search?tabs=azurecli%2Cpython&pivots=overview-azure-ai-search" target="_blank">Azure AI Search</a>

2. Action 工具s:
    - <a href="https://learn.microsoft.com/azure/ai-services/Agent/how-to/工具s/function-calling?tabs=python&pivots=overview" target="_blank">Function Calling</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/Agent/how-to/工具s/code-interpreter?tabs=python&pivots=overview" target="_blank">Code Interpreter</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/Agent/how-to/工具s/openapi-spec?tabs=python&pivots=overview" target="_blank">OpenAPI defined 工具s</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/Agent/how-to/工具s/azure-functions?pivots=overview" target="_blank">Azure Functions</a>

The Agent Service allows us to be able to use these 工具s together as a `工具set`. It also utilizes `threads` which keep track of the history of messages from a particular conversation.

Imagine you are a sales Agent at a company called Contoso. You want to develop a conversational Agent that can answer questions about your sales data.

The following image illustrates how you could use Azure AI Agent Service to analyze your sales data:

![Agentic Service In Action](./images/Agent-service-in-action.jpg)

To use any of these 工具s with the service we can create a client and define a 工具 or 工具set. To implement this practically we can use the following Python code. The 大型语言模型 will be able to look at the 工具set and decide whether to use the user created function, `fetch_sales_data_using_sqlite_query`, or the pre-built Code Interpreter depending on the user request.

```python 
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from fetch_sales_data_functions import fetch_sales_data_using_sqlite_query # fetch_sales_data_using_sqlite_query function which can be found in a fetch_sales_data_functions.py file.
from azure.ai.projects.models import 工具Set, Function工具, CodeInterpreter工具

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

# Initialize 工具set
工具set = 工具Set()

# Initialize function calling Agent with the fetch_sales_data_using_sqlite_query function and adding it to the 工具set
fetch_data_function = Function工具(fetch_sales_data_using_sqlite_query)
工具set.add(fetch_data_function)

# Initialize Code Interpreter 工具 and adding it to the 工具set. 
code_interpreter = code_interpreter = CodeInterpreter工具()
工具set.add(code_interpreter)

Agent = project_client.Agent.create_Agent(
    model="gpt-4o-mini", name="my-Agent", instructions="You are helpful Agent", 
    工具set=工具set
)
```

## 什么是 are the special considerations for using the 工具使用 Design 模式 to build trustworthy AI Agent?

A common concern with SQL dynamically generated by 大型语言模型s is security, particularly the risk of SQL injection or malicious actions, such as dropping or tampering with the database. While these concerns are valid, they can be effectively mitigated by properly configuring database access permissions. For most databases this involves configuring the database as read-only. For database services like PostgreSQL or Azure SQL, the app should be assigned a read-only (SELECT) role.

Running the app in a secure environment further enhances protection. In enterprise scenarios, data is typically extracted and transformed from operational systems into a read-only database or data warehouse with a user-friendly schema. This approach ensures that the data is secure, optimized for performance and accessibility, and that the app has restricted, read-only access.

## 示例代码s

- Python: [Agent 框架](./code_samples/04-python-Agent-框架.ipynb)
- .NET: [Agent 框架](./code_samples/04-dotnet-Agent-框架.md)

## Got More Questions about the 工具使用 Design 模式s?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.

## Additional Resources

- <a href="https://microsoft.github.io/build-your-first-Agent-with-azure-ai-Agent-service-workshop/" target="_blank">Azure AI Agent Service Workshop</a>
- <a href="https://github.com/Azure-Samples/contoso-creative-writer/tree/main/docs/workshop" target="_blank">Contoso Creative Writer 多 Agent 系统 Workshop</a>
- <a href="https://learn.microsoft.com/semantic-kernel/concepts/ai-services/chat-completion/function-calling/?pivots=programming-language-python#1-serializing-the-functions" target="_blank">Semantic Kernel Function Calling Tutorial</a>
- <a href="https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_Agent/openai_assistant/step3_assistant_工具_code_interpreter.py" target="_blank">Semantic Kernel Code Interpreter</a>
- <a href="https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/components/工具s.html" target="_blank">Autogen 工具s</a>

## 上一课

[Understanding Agentic Design 模式s](../03-Agentic-design-模式s/README.md)

## 下一课

[Agentic RAG](../05-Agentic-rag/README.md)
