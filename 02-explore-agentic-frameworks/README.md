[![Exploring AI Agent 框架s](./images/lesson-2-thumbnail.png)](https://youtu.be/ODwF-EZo_O8?si=1xoy_B9RNQfrYdF7)

> _(Click the image above to view video of this lesson)_

# Explore AI Agent 框架s

AI Agent 框架s are software platforms designed to simplify the creation, deployment, and management of AI Agent. These 框架s provide developers with pre-built components, abstractions, and 工具s that streamline the development of complex AI systems.

These 框架s help developers focus on the unique aspects of their applications by providing standardized approaches to common challenges in AI Agent development. They enhance scalability, accessibility, and efficiency in building AI systems.

## 简介 

This lesson will cover:

- What are AI Agent 框架s and what do they enable developers to achieve?
- How can teams use these to quickly prototype, iterate, and improve their Agent’s capabilities?
- What are the differences between the 框架s and 工具s created by Microsoft <a href="https://aka.ms/ai-Agent/autogen" target="_blank">AutoGen</a>, <a href="https://aka.ms/ai-Agent-beginners/semantic-kernel" target="_blank">Semantic Kernel</a>, and <a href="https://aka.ms/ai-Agent-beginners/ai-Agent-service" target="_blank">Azure AI Agent Service</a>?
- Can I integrate my existing Azure ecosystem 工具s directly, or do I need standalone solutions?
- What is Azure AI Agent service and how is this helping me?

## Learning goals

The goals of this lesson are to help you understand:

- The role of AI Agent 框架s in AI development.
- How to leverage AI Agent 框架s to build intelligent Agent.
- Key capabilities enabled by AI Agent 框架s.
- The differences between AutoGen, Semantic Kernel, and Azure AI Agent Service.

## 什么是 are AI Agent 框架s and what do they enable developers to do?

Traditional AI 框架s can help you integrate AI into your apps and make these apps better in the following ways:

- **Personalization**: AI can analyze user behavior and preferences to provide personalized recommendations, content, and experiences.
Example: Streaming services like Netflix use AI to suggest movies and shows based on viewing history, enhancing user engagement and satisfaction.
- **Automation and Efficiency**: AI can automate repetitive tasks, streamline workflows, and improve operational efficiency.
Example: Customer service apps use AI-powered chatbots to handle common inquiries, reducing response times and freeing up human Agent for more complex issues.
- **Enhanced User Experience**: AI can improve the overall user experience by providing intelligent features such as voice recognition, natural language processing, and predictive text.
Example: Virtual assistants like Siri and Google Assistant use AI to understand and respond to voice commands, making it easier for users to interact with their devices.

### That all sounds great right, so why do we need the AI Agent 框架?

AI Agent 框架s represent something more than just AI 框架s. They are designed to enable the creation of intelligent Agent that can interact with users, other Agent, and the environment to achieve specific goals. These Agent can exhibit autonomous behavior, make decisions, and adapt to changing conditions. Let's look at some key capabilities enabled by AI Agent 框架s:

- **Agent Collaboration and Coordination**: Enable the creation of multiple AI Agent that can work together, communicate, and coordinate to solve complex tasks.
- **Task Automation and Management**: Provide mechanisms for automating multi-step workflows, task delegation, and dynamic task management among Agent.
- **Contextual Understanding and Adaptation**: Equip Agent with the ability to understand context, adapt to changing environments, and make decisions based on real-time information.

So in summary, Agent allow you to do more, to take automation to the next level, to create more intelligent systems that can adapt and learn from their environment.

## How to quickly prototype, iterate, and improve the Agent’s capabilities?

This is a fast-moving landscape, but there are some things that are common across most AI Agent 框架s that can help you quickly prototype and iterate namely module components, collaborative 工具s, and real-time learning. Let's dive into these:

- **Use Modular Components**: AI SDKs offer pre-built components such as AI and 记忆 connectors, function calling using natural language or code plugins, prompt templates, and more.
- **Leverage Collaborative 工具s**: Design Agent with specific roles and tasks, enabling them to test and refine collaborative workflows.
- **Learn in Real-Time**: Implement feedback loops where Agent learn from interactions and adjust their behavior dynamically.

### Use Modular Components

SDKs like Microsoft Semantic Kernel and LangChain offer pre-built components such as AI connectors, prompt templates, and 记忆 management.

**How teams can use these**: Teams can quickly assemble these components to create a functional prototype without starting from scratch, allowing for rapid experimentation and iteration.

**How it works in practice**: You can use a pre-built parser to extract information from user input, a 记忆 module to store and retrieve data, and a prompt generator to interact with users, all without having to build these components from scratch.

**Example code**. Let's look at examples of how you can use a pre-built AI Connector with Semantic Kernel Python and .Net that uses auto-function calling to have the model respond to user input:

``` python
# Semantic Kernel Python Example

import asyncio
from typing import Annotated

from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
from semantic_kernel.kernel import Kernel

# Define a ChatHistory object to hold the conversation's context
chat_history = ChatHistory()
chat_history.add_user_message("I'd like to go to New York on January 1, 2025")


# Define a sample plugin that contains the function to book travel
class BookTravelPlugin:
    """A Sample Book Travel Plugin"""

    @kernel_function(name="book_flight", description="Book travel given location and date")
    async def book_flight(
        self, date: Annotated[str, "The date of travel"], location: Annotated[str, "The location to travel to"]
    ) -> str:
        return f"Travel was booked to {location} on {date}"

# Create the Kernel
kernel = Kernel()

# Add the sample plugin to the Kernel object
kernel.add_plugin(BookTravelPlugin(), plugin_name="book_travel")

# Define the Azure OpenAI AI Connector
chat_service = AzureChatCompletion(
    deployment_name="YOUR_DEPLOYMENT_NAME", 
    api_key="YOUR_API_KEY", 
    endpoint="https://<your-resource>.azure.openai.com/",
)

# Define the request settings to configure the model with auto-function calling
request_settings = AzureChatPromptExecutionSettings(function_choice_behavior=FunctionChoiceBehavior.Auto())


async def main():
    # Make the request to the model for the given chat history and request settings
    # The Kernel contains the sample that the model will request to invoke
    response = await chat_service.get_chat_message_content(
        chat_history=chat_history, settings=request_settings, kernel=kernel
    )
    assert response is not None

    """
    Note: In the auto function calling process, the model determines it can invoke the 
    `BookTravelPlugin` using the `book_flight` function, supplying the necessary arguments. 
    
    For example:

    "工具_calls": [
        {
            "id": "call_abc123",
            "type": "function",
            "function": {
                "name": "BookTravelPlugin-book_flight",
                "arguments": "{'location': 'New York', 'date': '2025-01-01'}"
            }
        }
    ]

    Since the location and date arguments are required (as defined by the kernel function), if the 
    model lacks either, it will prompt the user to provide them. For instance:

    User: Book me a flight to New York.
    Model: Sure, I'd love to help you book a flight. Could you please specify the date?
    User: I want to travel on January 1, 2025.
    Model: Your flight to New York on January 1, 2025, has been successfully booked. Safe travels!
    """

    print(f"`{response}`")
    # Example AI Model Response: `Your flight to New York on January 1, 2025, has been successfully booked. Safe travels! ✈️🗽`

    # Add the model's response to our chat history context
    chat_history.add_assistant_message(response.content)


if __name__ == "__main__":
    asyncio.run(main())
```
```csharp
// Semantic Kernel C# example

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using System.ComponentModel;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;

ChatHistory chatHistory = [];
chatHistory.AddUserMessage("I'd like to go to New York on January 1, 2025");

var kernelBuilder = Kernel.CreateBuilder();
kernelBuilder.AddAzureOpenAIChatCompletion(
    deploymentName: "NAME_OF_YOUR_DEPLOYMENT",
    apiKey: "YOUR_API_KEY",
    endpoint: "YOUR_AZURE_ENDPOINT"
);
kernelBuilder.Plugins.AddFromType<BookTravelPlugin>("BookTravel"); 
var kernel = kernelBuilder.Build();

var settings = new AzureOpenAIPromptExecutionSettings()
{
    FunctionChoiceBehavior = FunctionChoiceBehavior.Auto()
};

var chatCompletion = kernel.GetRequiredService<IChatCompletionService>();

var response = await chatCompletion.GetChatMessageContentAsync(chatHistory, settings, kernel);

/*
Behind the scenes, the model recognizes the 工具 to call, what arguments it already has (location) and (date)
{

"工具_calls": [
    {
        "id": "call_abc123",
        "type": "function",
        "function": {
            "name": "BookTravelPlugin-book_flight",
            "arguments": "{'location': 'New York', 'date': '2025-01-01'}"
        }
    }
]
*/

Console.WriteLine(response.Content);
chatHistory.AddMessage(response!.Role, response!.Content!);

// Example AI Model Response: Your flight to New York on January 1, 2025, has been successfully booked. Safe travels! ✈️🗽

// Define a plugin that contains the function to book travel
public class BookTravelPlugin
{
    [KernelFunction("book_flight")]
    [Description("Book travel given location and date")]
    public async Task<string> BookFlight(DateTime date, string location)
    {
        return await Task.FromResult( $"Travel was booked to {location} on {date}");
    }
}
```

What you can see from this example is how you can leverage a pre-built parser to extract key information from user input, such as the origin, destination, and date of a flight booking request. This modular approach allows you to focus on the high-level logic.

### Leverage Collaborative 工具s

框架s like CrewAI, Microsoft AutoGen, and Semantic Kernel facilitate the creation of multiple Agent that can work together.

**How teams can use these**: Teams can design Agent with specific roles and tasks, enabling them to test and refine collaborative workflows and improve overall system efficiency.

**How it works in practice**: You can create a team of Agent where each Agent has a specialized function, such as data retrieval, analysis, or decision-making. These Agent can communicate and share information to achieve a common goal, such as answering a user query or completing a task.

**Example code (AutoGen)**:

```python
# creating Agent, then create a round robin schedule where they can work together, in this case in order

# Data Retrieval Agent
# Data Analysis Agent
# Decision Making Agent

Agent_retrieve = AssistantAgent(
    name="dataretrieval",
    model_client=model_client,
    工具s=[retrieve_工具],
    system_message="Use 工具s to solve tasks."
)

Agent_analyze = AssistantAgent(
    name="dataanalysis",
    model_client=model_client,
    工具s=[analyze_工具],
    system_message="Use 工具s to solve tasks."
)

# conversation ends when user says "APPROVE"
termination = TextMentionTermination("APPROVE")

user_proxy = UserProxyAgent("user_proxy", input_func=input)

team = RoundRobinGroupChat([Agent_retrieve, Agent_analyze, user_proxy], termination_condition=termination)

stream = team.run_stream(task="Analyze data", max_turns=10)
# Use asyncio.run(...) when running in a script.
await Console(stream)
```

What you see in the previous code is how you can create a task that involves multiple Agent working together to analyze data. Each Agent performs a specific function, and the task is executed by coordinating the Agent to achieve the desired outcome. By creating dedicated Agent with specialized roles, you can improve task efficiency and performance.

### Learn in Real-Time

Advanced 框架s provide capabilities for real-time context understanding and adaptation.

**How teams can use these**: Teams can implement feedback loops where Agent learn from interactions and adjust their behavior dynamically, leading to continuous improvement and refinement of capabilities.

**How it works in practice**: Agent can analyze user feedback, environmental data, and task outcomes to update their knowledge base, adjust decision-making algorithms, and improve performance over time. This iterative learning process enables Agent to adapt to changing conditions and user preferences, enhancing overall system effectiveness.

## 什么是 are the differences between the 框架s AutoGen, Semantic Kernel and Azure AI Agent Service?

There are many ways to compare these 框架s, but let's look at some key differences in terms of their design, capabilities, and target use cases:

## AutoGen

AutoGen is an open-source 框架 developed by Microsoft Research's AI Frontiers Lab. It focuses on event-driven, distributed *Agentic* applications, enabling multiple 大型语言模型s and SLMs, 工具s, and advanced multi-Agent design 模式s.

AutoGen is built around the core concept of Agent, which are autonomous entities that can perceive their environment, make decisions, and take actions to achieve specific goals. Agent communicate through asynchronous messages, allowing them to work independently and in parallel, enhancing system scalability and responsiveness.

<a href="https://en.wikipedia.org/wiki/Actor_model" target="_blank">Agent are based on the actor model</a>. According to Wikipedia, an actor is _the basic building block of concurrent computation. In response to a message it receives, an actor can: make local decisions, create more actors, send more messages, and determine how to respond to the next message received_.

**Use Cases**: Automating code generation, data analysis tasks, and building custom Agent for planning and research functions.

Here are some important core concepts of AutoGen:

- **Agent**. An Agent is a software entity that:
  - **Communicates via messages**, these messages can be synchronous or asynchronous.
  - **Maintains its own state**, which can be modified by incoming messages.
  - **Performs actions** in response to received messages or changes in its state. These actions may modify the Agent’s state and produce external effects, such as updating message logs, sending new messages, executing code, or making API calls.
    
  Here you have a short code snippet in which you create your own Agent with Chat capabilities:

    ```python
    from autogen_Agentchat.Agent import AssistantAgent
    from autogen_Agentchat.messages import TextMessage
    from autogen_ext.models.openai import OpenAIChatCompletionClient


    class MyAgent(RoutedAgent):
        def __init__(self, name: str) -> None:
            super().__init__(name)
            model_client = OpenAIChatCompletionClient(model="gpt-4o")
            self._delegate = AssistantAgent(name, model_client=model_client)
    
        @message_handler
        async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
            print(f"{self.id.type} received message: {message.content}")
            response = await self._delegate.on_messages(
                [TextMessage(content=message.content, source="user")], ctx.cancellation_token
            )
            print(f"{self.id.type} responded: {response.chat_message.content}")
    ```
    
    In the previous code, `MyAgent` has been created and inherits from `RoutedAgent`. It has a message handler that prints the content of the message and then sends a response using the `AssistantAgent` delegate. Especially note how we assign to `self._delegate` an instance of `AssistantAgent` which is a pre-built Agent that can handle chat completions.


    Let's let AutoGen know about this Agent type and kick off the program next:

    ```python
    
    # main.py
    runtime = SingleThreadedAgentRuntime()
    await MyAgent.register(runtime, "my_Agent", lambda: MyAgent())

    runtime.start()  # Start processing messages in the background.
    await runtime.send_message(MyMessageType("Hello, World!"), AgentId("my_Agent", "default"))
    ```

    In the previous code the Agent are registered with the runtime and then a message is sent to the Agent resulting in the following output:

    ```text
    # Output from the console:
    my_Agent received message: Hello, World!
    my_assistant received message: Hello, World!
    my_assistant responded: Hello! How can I assist you today?
    ```

- **Multi Agent**. AutoGen supports the creation of multiple Agent that can work together to achieve complex tasks. Agent can communicate, share information, and coordinate their actions to solve problems more efficiently. To create a multi-Agent system, you can define different types of Agent with specialized functions and roles, such as data retrieval, analysis, decision-making, and user interaction. Let's see how such a creation looks like so we get a sense of it:

    ```python
    editor_description = "Editor for planning and reviewing the content."

    # Example of declaring an Agent
    editor_Agent_type = await EditorAgent.register(
    runtime,
    editor_topic_type,  # Using topic type as the Agent type.
    lambda: EditorAgent(
        description=editor_description,
        group_chat_topic_type=group_chat_topic_type,
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-2024-08-06",
            # api_key="YOUR_API_KEY",
        ),
        ),
    )

    # remaining declarations shortened for brevity

    # Group chat
    group_chat_manager_type = await GroupChatManager.register(
    runtime,
    "group_chat_manager",
    lambda: GroupChatManager(
        participant_topic_types=[writer_topic_type, illustrator_topic_type, editor_topic_type, user_topic_type],
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-2024-08-06",
            # api_key="YOUR_API_KEY",
        ),
        participant_descriptions=[
            writer_description, 
            illustrator_description, 
            editor_description, 
            user_description
        ],
        ),
    )
    ```

    In the previous code we have a `GroupChatManager` that is registered with the runtime. This manager is responsible for coordinating the interactions between different types of Agent, such as writers, illustrators, editors, and users.

- **Agent Runtime**. The 框架 provides a runtime environment, enabling communication between Agent, manages their identities and lifecycles, and enforce security and privacy boundaries. This means that you can run your Agent in a secure and controlled environment, ensuring that they can interact safely and efficiently. There are two runtimes of interest:
  - **Stand-alone runtime**. This is a good choice for single-process applications where all Agent are implemented in the same programming language and run in the same process. Here's an illustration of how it works:
  
    <a href="https://microsoft.github.io/autogen/stable/_images/architecture-standalone.svg" target="_blank">Stand-alone runtime</a>   
Application stack

    *Agent communicate via messages through the runtime, and the runtime manages the lifecycle of Agent*

  - **Distributed Agent runtime**, is suitable for multi-process applications where Agent may be implemented in different programming languages and running on different machines. Here's an illustration of how it works:
  
    <a href="https://microsoft.github.io/autogen/stable/_images/architecture-distributed.svg" target="_blank">Distributed runtime</a>

## Semantic Kernel + Agent 框架

Semantic Kernel is an enterprise-ready AI Orchestration SDK. It consists of AI and 记忆 connectors, along with an Agent 框架.

Let's first cover some core components:

- **AI Connectors**: This is an interface with external AI services and data sources for use in both Python and C#.

  ```python
  # Semantic Kernel Python
  from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
  from semantic_kernel.kernel import Kernel

  kernel = Kernel()
  kernel.add_service(
    AzureChatCompletion(
        deployment_name="your-deployment-name",
        api_key="your-api-key",
        endpoint="your-endpoint",
    )
  )
  ```  

    ```csharp
    // Semantic Kernel C#
    using Microsoft.SemanticKernel;

    // Create kernel
    var builder = Kernel.CreateBuilder();
    
    // Add a chat completion service:
    builder.Services.AddAzureOpenAIChatCompletion(
        "your-resource-name",
        "your-endpoint",
        "your-resource-key",
        "deployment-model");
    var kernel = builder.Build();
    ```

    Here you have a simple example of how you can create a kernel and add a chat completion service. Semantic Kernel creates a connection to an external AI service, in this case, Azure OpenAI Chat Completion.

- **Plugins**: These encapsulate functions that an application can use. There are both ready-made plugins and custom ones you can create. A related concept is "prompt functions." Instead of providing natural language cues for function invocation, you broadcast certain functions to the model. Based on the current chat context, the model may choose to call one of these functions to complete a request or query. Here's an example:

  ```python
  from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion


  async def main():
      from semantic_kernel.functions import KernelFunctionFromPrompt
      from semantic_kernel.kernel import Kernel

      kernel = Kernel()
      kernel.add_service(AzureChatCompletion())

      user_input = input("User Input:> ")

      kernel_function = KernelFunctionFromPrompt(
          function_name="SummarizeText",
          prompt="""
          Summarize the provided unstructured text in a sentence that is easy to understand.
          Text to summarize: {{$user_input}}
          """,
      )

      response = await kernel_function.invoke(kernel=kernel, user_input=user_input)
      print(f"Model Response: {response}")

      """
      Sample Console Output:

      User Input:> I like dogs
      Model Response: The text expresses a preference for dogs.
      """


  if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
  ```

    ```csharp
    var userInput = Console.ReadLine();

    // Define semantic function inline.
    string skPrompt = @"Summarize the provided unstructured text in a sentence that is easy to understand.
                        Text to summarize: {{$userInput}}";
    
    // create the function from the prompt
    KernelFunction summarizeFunc = kernel.CreateFunctionFromPrompt(
        promptTemplate: skPrompt,
        functionName: "SummarizeText"
    );

    //then import into the current kernel
    kernel.ImportPluginFromFunctions("SemanticFunctions", [summarizeFunc]);

    ```

    Here, you first have a template prompt `skPrompt` that leaves room for the user to input text, `$userInput`. Then you create the kernel function `SummarizeText` and then import it into the kernel with the plugin name `SemanticFunctions`. Note the name of the function that helps Semantic Kernel understand what the function does and when it should be called.

- **Native function**: There's also native functions that the 框架 can call directly to carry out the task. Here's an example of such a function retrieving the content from a file:

    ```csharp
    public class NativeFunctions {

        [SKFunction, Description("Retrieve content from local file")]
        public async Task<string> RetrieveLocalFile(string fileName, int maxSize = 5000)
        {
            string content = await File.ReadAllTextAsync(fileName);
            if (content.Length <= maxSize) return content;
            return content.Substring(0, maxSize);
        }
    }
    
    //Import native function
    string plugInName = "NativeFunction";
    string functionName = "RetrieveLocalFile";

   //To add the functions to a kernel use the following function
    kernel.ImportPluginFromType<NativeFunctions>();

    ```

- **记忆**:  Abstracts and simplifies context management for AI apps. The idea with 记忆 is that this is something the 大型语言模型 should know about. You can store this information in a vector store which ends up being an in-记忆 database or a vector database or similar. Here's an example of a very simplified scenario where *facts* are added to the 记忆:

    ```csharp
    var facts = new Dictionary<string,string>();
    facts.Add(
        "Azure Machine Learning; https://learn.microsoft.com/azure/machine-learning/",
        @"Azure Machine Learning is a cloud service for accelerating and
        managing the machine learning project lifecycle. Machine learning professionals,
        data scientists, and engineers can use it in their day-to-day workflows"
    );
    
    facts.Add(
        "Azure SQL Service; https://learn.microsoft.com/azure/azure-sql/",
        @"Azure SQL is a family of managed, secure, and intelligent products
        that use the SQL Server database engine in the Azure cloud."
    );
    
    string 记忆CollectionName = "SummarizedAzureDocs";
    
    foreach (var fact in facts) {
        await 记忆Builder.SaveReferenceAsync(
            collection: 记忆CollectionName,
            description: fact.Key.Split(";")[1].Trim(),
            text: fact.Value,
            externalId: fact.Key.Split(";")[2].Trim(),
            externalSourceName: "Azure Documentation"
        );
    }
    ```

    These facts are then stored in the 记忆 collection `SummarizedAzureDocs`. This is a very simplified example, but you can see how you can store information in the 记忆 for the 大型语言模型 to use.

So that's the basics of the Semantic Kernel 框架, what about the Agent 框架?

## Azure AI Agent Service

Azure AI Agent Service is a more recent addition, introduced at Microsoft Ignite 2024. It allows for the development and deployment of AI Agent with more flexible models, such as directly calling open-source 大型语言模型s like Llama 3, Mistral, and Cohere.

Azure AI Agent Service provides stronger enterprise security mechanisms and data storage methods, making it suitable for enterprise applications. 

It works out-of-the-box with multi-Agent orchestration 框架s like AutoGen and Semantic Kernel.

This service is currently in Public Preview and supports Python and C# for building Agent.

Using Semantic Kernel Python, we can create an Azure AI Agent with a user-defined plugin:

```python
import asyncio
from typing import Annotated

from azure.identity.aio import DefaultAzureCredential

from semantic_kernel.Agent import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents import AuthorRole
from semantic_kernel.functions import kernel_function


# Define a sample plugin for the sample
class MenuPlugin:
    """A sample Menu Plugin used for the concept sample."""

    @kernel_function(description="Provides a list of specials from the menu.")
    def get_specials(self) -> Annotated[str, "Returns the specials from the menu."]:
        return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """

    @kernel_function(description="Provides the price of the requested menu item.")
    def get_item_price(
        self, menu_item: Annotated[str, "The name of the menu item."]
    ) -> Annotated[str, "Returns the price of the menu item."]:
        return "$9.99"


async def main() -> None:
    ai_Agent_settings = AzureAIAgentSettings.create()

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(
            credential=creds,
            conn_str=ai_Agent_settings.project_connection_string.get_secret_value(),
        ) as client,
    ):
        # Create Agent definition
        Agent_definition = await client.Agent.create_Agent(
            model=ai_Agent_settings.model_deployment_name,
            name="Host",
            instructions="Answer questions about the menu.",
        )

        # Create the AzureAI Agent using the defined client and Agent definition
        Agent = AzureAIAgent(
            client=client,
            definition=Agent_definition,
            plugins=[MenuPlugin()],
        )

        # Create a thread to hold the conversation
        # If no thread is provided, a new thread will be
        # created and returned with the initial response
        thread: AzureAIAgentThread | None = None

        user_inputs = [
            "Hello",
            "What is the special soup?",
            "How much does that cost?",
            "Thank you",
        ]

        try:
            for user_input in user_inputs:
                print(f"# User: '{user_input}'")
                # Invoke the Agent for the specified thread
                response = await Agent.get_response(
                    messages=user_input,
                    thread_id=thread,
                )
                print(f"# {response.name}: {response.content}")
                thread = response.thread
        finally:
            await thread.delete() if thread else None
            await client.Agent.delete_Agent(Agent.id)


if __name__ == "__main__":
    asyncio.run(main())
```

### Core concepts

Azure AI Agent Service has the following core concepts:

- **Agent**. Azure AI Agent Service integrates with Azure AI Foundry. Within AI Foundry, an AI Agent acts as a "smart" microservice that can be used to answer questions (RAG), perform actions, or completely automate workflows. It achieves this by combining the power of generative AI models with 工具s that allow it to access and interact with real-world data sources. Here's an example of an Agent:

    ```python
    Agent = project_client.Agent.create_Agent(
        model="gpt-4o-mini",
        name="my-Agent",
        instructions="You are helpful Agent",
        工具s=code_interpreter.definitions,
        工具_resources=code_interpreter.resources,
    )
    ```

    In this example, an Agent is created with the model `gpt-4o-mini`, a name `my-Agent`, and instructions `You are helpful Agent`. The Agent is equipped with 工具s and resources to perform code interpretation tasks.

- **Thread and messages**. The thread is another important concept. It represents a conversation or interaction between an Agent and a user. Threads can be used to track the progress of a conversation, store context information, and manage the state of the interaction. Here's an example of a thread:

    ```python
    thread = project_client.Agent.create_thread()
    message = project_client.Agent.create_message(
        thread_id=thread.id,
        role="user",
        content="Could you please create a bar chart for the operating profit using the following data and provide the file to me? Company A: $1.2 million, Company B: $2.5 million, Company C: $3.0 million, Company D: $1.8 million",
    )
    
    # Ask the Agent to perform work on the thread
    run = project_client.Agent.create_and_process_run(thread_id=thread.id, Agent_id=Agent.id)
    
    # Fetch and log all messages to see the Agent's response
    messages = project_client.Agent.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
    ```

    In the previous code, a thread is created. Thereafter, a message is sent to the thread. By calling `create_and_process_run`, the Agent is asked to perform work on the thread. Finally, the messages are fetched and logged to see the Agent's response. The messages indicate the progress of the conversation between the user and the Agent. It's also important to understand that the messages can be of different types such as text, image, or file, that is the Agent work has resulted in for example an image or a text response for example. As a developer, you can then use this information to further process the response or present it to the user.

- **Integrates with other AI 框架s**. Azure AI Agent service can interact with other 框架s like AutoGen and Semantic Kernel, which means you can build part of your app in one of these 框架s and for example using the Agent service as an orchestrator or you can build everything in the Agent service.

**Use Cases**: Azure AI Agent Service is designed for enterprise applications that require secure, scalable, and flexible AI Agent deployment.

## 什么是's the difference between these 框架s?
 
It does sound like there is a lot of overlap between these 框架s, but there are some key differences in terms of their design, capabilities, and target use cases:
 
- **AutoGen**: Is an experimentation 框架 focused on leading-edge research on multi-Agent systems. It is the best place to experiment and prototype sophisticated multi-Agent systems.
- **Semantic Kernel**: Is a production-ready Agent library for building enterprise Agentic applications. Focuses on event-driven, distributed Agentic applications, enabling multiple 大型语言模型s and SLMs, 工具s, and single/multi-Agent design 模式s.
- **Azure AI Agent Service**: Is a platform and deployment service in Azure Foundry for Agent. It offers building connectivity to services support by Azure Found like Azure OpenAI, Azure AI Search, Bing Search and code execution.
 
Still not sure which one to choose?

### Use Cases
 
Let's see if we can help you by going through some common use cases:
 
> Q: I'm experimenting, learning and building proof-of-concept Agent applications, and I want to be able to build and experiment quickly
>

>A: AutoGen would be a good choice for this scenario, as it focuses on event-driven, distributed Agentic applications and supports advanced multi-Agent design 模式s.

> Q: What makes AutoGen a better choice than Semantic Kernel and Azure AI Agent Service for this use case?
>
> A: AutoGen is specifically designed for event-driven, distributed Agentic applications, making it well-suited for automating code generation and data analysis tasks. It provides the necessary 工具s and capabilities to build complex multi-Agent systems efficiently.

>Q: Sounds like Azure AI Agent Service could work here too, it has 工具s for code generation and more?

>
> A: Yes, Azure AI Agent Service is a platform service for Agent and add built-in capabilities for multiple models, Azure AI Search, Bing Search and Azure Functions. It makes it easy to build your Agent in the Foundry Portal and deploy them at scale.
 
> Q: I'm still confused just give me one option
>
> A: A great choice is to build your application in Semantic Kernel first and then use Azure AI Agent Service to deploy your Agent. This approach allows you to easily persist your Agent while leveraging the power to build multi-Agent systems in Semantic Kernel. Additionally, Semantic Kernel has a connector in AutoGen, making it easy to use both 框架s together.
 
Let's summarize the key differences in a table:

| 框架 | Focus | Core Concepts | Use Cases |
| --- | --- | --- | --- |
| AutoGen | Event-driven, distributed Agentic applications | Agent, Personas, Functions, Data | Code generation, data analysis tasks |
| Semantic Kernel | Understanding and generating human-like text content | Agent, Modular Components, Collaboration | Natural language understanding, content generation |
| Azure AI Agent Service | Flexible models, enterprise security, Code generation, 工具 calling | Modularity, Collaboration, Process Orchestration | Secure, scalable, and flexible AI Agent deployment |

What's the ideal use case for each of these 框架s?

## Can I integrate my existing Azure ecosystem 工具s directly, or do I need standalone solutions?

The answer is yes, you can integrate your existing Azure ecosystem 工具s directly with Azure AI Agent Service especially, this because it has been built to work seamlessly with other Azure services. You could for example integrate Bing, Azure AI Search, and Azure Functions. There's also deep integration with Azure AI Foundry.

For AutoGen and Semantic Kernel, you can also integrate with Azure services, but it may require you to call the Azure services from your code. Another way to integrate is to use the Azure SDKs to interact with Azure services from your Agent. Additionally, like was mentioned, you can use Azure AI Agent Service as an orchestrator for your Agent built in AutoGen or Semantic Kernel which would give easy access to the Azure ecosystem.

## 示例代码s

- Python: [Agent 框架](./code_samples/02-python-Agent-框架.ipynb)
- .NET: [Agent 框架](./code_samples/02-dotnet-Agent-框架.md)

## Got More Questions about AI Agent 框架s?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-Agent/discord) to meet with other learners, attend office hours and get your AI Agent questions answered.

## References

- <a href="https://techcommunity.microsoft.com/blog/azure-ai-services-blog/introducing-azure-ai-Agent-service/4298357" target="_blank">Azure Agent Service</a>
- <a href="https://devblogs.microsoft.com/semantic-kernel/microsofts-Agentic-ai-框架s-autogen-and-semantic-kernel/" target="_blank">Semantic Kernel and AutoGen</a>
- <a href="https://learn.microsoft.com/semantic-kernel/框架s/Agent/?pivots=programming-language-python" target="_blank">Semantic Kernel Python Agent 框架</a>
- <a href="https://learn.microsoft.com/semantic-kernel/框架s/Agent/?pivots=programming-language-csharp" target="_blank">Semantic Kernel .Net Agent 框架</a>
- <a href="https://learn.microsoft.com/azure/ai-services/Agent/overview" target="_blank">Azure AI Agent service</a>
- <a href="https://techcommunity.microsoft.com/blog/educatordeveloperblog/using-azure-ai-Agent-service-with-autogen--semantic-kernel-to-build-a-multi-agen/4363121" target="_blank">Using Azure AI Agent Service with AutoGen / Semantic Kernel to build a multi-Agent's solution</a>

## 上一课

[AI Agent 入门 and Agent Use Cases](../01-intro-to-ai-Agent/README.md)

## 下一课

[Understanding Agentic Design 模式s](../03-Agentic-design-模式s/README.md)
