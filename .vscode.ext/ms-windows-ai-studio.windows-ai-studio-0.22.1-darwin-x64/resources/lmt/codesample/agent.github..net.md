### Microsoft Agent Framework code samples (.NET)

#### Quick Start
Connect GitHub model first, then create the agent instance:

``` csharp
using System.ClientModel;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Agents;
using OpenAI;
namespace MyAgent;
public static class Program
{
    public static async Task Main(string[] args)
    {
        const string AgentName = "MyAgent";
        const string AgentInstructions = "You are a helpful agent.";
        // Create OpenAIClient based ChatAgent
        AIAgent agent = new OpenAIClient(
            new ApiKeyCredential("<GITHUB_TOKEN>"),
            new OpenAIClientOptions
            {
                Endpoint = new Uri("https://models.github.ai/inference")
            }
        )
        .GetChatClient("<model-id>")
        .CreateAIAgent(
            AgentInstructions,
            AgentName
        );

        var response = await agent.RunAsync("hello");
        Console.WriteLine($"Agent: {response}"); // Hello! How can I assist you today?
    }
}
```

#### Add tool
Tools (or Function Callings) can let Agent interact with external APIs or services, enhancing its capabilities.

``` csharp
using System.ComponentModel;
using Microsoft.Extensions.AI;
//...
public static class Program
{
    [Description("Get the weather for a given location.")]
    public static string GetWeather([Description("The location to get the weather for.")] string location)
    {
        Random rand = new();
        string[] conditions = { "sunny", "cloudy", "rainy", "stormy" };
        return $"The weather in {location} is {conditions[rand.Next(0, 4)]} with a high of {rand.Next(10, 30)}°C.";
    }

    public static async Task Main(string[] args)
    {
        AIAgent agent =
        // ...
        .CreateAIAgent(
            AgentInstructions,
            AgentName,
            tools: [AIFunctionFactory.Create(GetWeather)]
        );

        var response = await agent.RunAsync("What's the weather like in Seattle?");
        Console.WriteLine($"Agent: {response}"); // The weather in Seattle is rainy with a high of 18°C.
    }
}
```

#### Multi-turn Conversation with Thread
Thread persistence across multiple conversations.

``` csharp
//...
public static class Program
{
    // ...
    public static async Task Main(string[] args)
    {
        AIAgent agent =
        // ...
        .CreateAIAgent(
            //...
        );

        // Create a new thread that will be reused
        AgentThread thread = agent.GetNewThread();

        // First conversation
        var response1 = await agent.RunAsync("What's the weather like in Seattle?", thread);
        Console.WriteLine($"Agent: {response1}"); // The weather in Seattle is rainy with a high of 18°C.

        // Second conversation using the same thread - maintains context
        var response2 = await agent.RunAsync("Pardon?", thread);
        Console.WriteLine($"Agent: {response2}"); // Sure. The weather in Seattle is rainy with a high of 18°C.
    }
}
```
