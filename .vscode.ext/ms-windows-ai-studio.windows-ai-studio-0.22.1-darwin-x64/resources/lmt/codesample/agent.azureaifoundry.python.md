### Microsoft Agent Framework code samples (Python)

#### Quick Start
Connect foundry model using FoundryChatClient, then create the agent instance:

``` python
from agent_framework import ChatAgent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import DefaultAzureCredential

async def quick_start() -> None:
    # Since no Agent ID is provided, the agent will be automatically created
    # and deleted after getting response
    async with ChatAgent(
        chat_client=FoundryChatClient(
            project_endpoint="<your-foundry-project-endpoint>",
            model_deployment_name="<your-foundry-model-deployment>",
            async_credential=DefaultAzureCredential(),
            agent_name="MyAgent",
        ),
        instructions="You are a helpful agent.",
    ) as agent:
        result=await agent.run("hello");
        print(f"Agent: {result.text}") # Hello! How can I assist you today?
```

#### Add tool
Tools (or Function Callings) can let Agent interact with external APIs or services, enhancing its capabilities.

``` python
from random import randint
from typing import Annotated

# Define tool(s) and add to 'ChatAgent'
def get_weather(
    location: Annotated[str, "The location to get the weather for."],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

async def quick_start_tools() -> None:
    #...
    async with ChatAgent(
        chat_client=FoundryChatClient(
            project_endpoint="<your-foundry-project-endpoint>",
            model_deployment_name="<your-foundry-model-deployment>",
            async_credential=DefaultAzureCredential(),
            agent_name="MyAgent",
        ),
        instructions="You are a helpful agent.",
        tools=[get_weather],
    ) as agent:
        result=await agent.run("What's the weather like in Seattle?")
        print(f"Agent: {result.text}") # The weather in Seattle is rainy with a high of 18°C.
```

#### Multi-turn Conversation with Thread
Thread persistence across multiple conversations.

``` python
async def quick_start_thread() -> None:
    #...
    async with ChatAgent(
        ...
    ) as agent:
        # Create a new thread that will be reused
        thread = agent.get_new_thread()

        # First conversation
        result1 = await agent.run("What's the weather like in Seattle?", thread=thread)
        print(f"Agent: {result1.text}") # The weather in Seattle is rainy with a high of 18°C.

        # Second conversation using the same thread - maintains context
        result2 = await agent.run("Pardon?", thread=thread)
        print(f"Agent: {result2.text}") # Sure. The weather in Seattle is rainy with a high of 18°C.
```
