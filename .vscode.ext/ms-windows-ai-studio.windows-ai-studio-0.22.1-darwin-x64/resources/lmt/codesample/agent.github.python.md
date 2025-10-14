### Microsoft Agent Framework code samples (Python)

#### Quick Start
Connect GitHub model first, then create the agent instance:

``` python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI

async def quick_start() -> None:
    openaiClient=AsyncOpenAI(
        base_url="https://models.github.ai/inference",
        api_key="<GITHUB_TOKEN>",
    )
    chatClient=OpenAIChatClient(
        async_client=openaiClient,
        ai_model_id="<model-id>"
    )
    agent=ChatAgent(
        chat_client=chatClient,
        name="MyAgent",
        instructions="You are a helpful agent.",
    )
    
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
    agent=ChatAgent(
        chat_client=chatClient,
        name="MyAgent",
        instructions="You are a helpful agent.",
        tools=[get_weather],
    )

    result=await agent.run("What's the weather like in Seattle?");
    print(f"Agent: {result.text}") # The weather in Seattle is rainy with a high of 18°C.
```

#### Multi-turn Conversation with Thread
Thread persistence across multiple conversations.

``` python
async def quick_start_thread() -> None:
    #...
    agent=ChatAgent(
        # settings...
    )
    # Create a new thread that will be reused
    thread = agent.get_new_thread()

    # First conversation
    result1 = await agent.run("What's the weather like in Seattle?", thread=thread)
    print(f"Agent: {result1.text}") # The weather in Seattle is rainy with a high of 18°C.

    # Second conversation using the same thread - maintains context
    result2 = await agent.run("Pardon?", thread=thread)
    print(f"Agent: {result2.text}") # Sure. The weather in Seattle is rainy with a high of 18°C.
```
