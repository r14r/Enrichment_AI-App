### Foundation Patterns via Microsoft Agent Framework (Python)

These samples introduce the core ideas of executors, edges, agents in workflows, and streaming.

#### 1. Executors and edges
```python
from agent_framework.workflow import (
    Executor,
    WorkflowBuilder,
    WorkflowCompletedEvent,
    WorkflowContext,
    executor,
    handler,
)

"""
Foundational patterns: Executors and edges

What this example shows
- Two ways to define a unit of work (an Executor node):
    1) Custom class that subclasses Executor with an async method marked by @handler.
         Signature: (text: str, ctx: WorkflowContext[str]) -> None. The typed ctx
         advertises the type this node emits via ctx.send_message(...).
    2) Standalone async function decorated with @executor using the same signature.
         Simple steps can use this form; a terminal step can emit a
         WorkflowCompletedEvent to end the workflow.

- Fluent WorkflowBuilder API:
    add_edge(A, B) to connect nodes, set_start_executor(A), then build() -> Workflow.

- Running and results:
    workflow.run(initial_input) executes the graph. The last node emits a
    WorkflowCompletedEvent that carries the final result.
"""


# Example 1: A custom Executor subclass
# ------------------------------------
#
# Subclassing Executor lets you define a named node with lifecycle hooks if needed.
# The work itself is implemented in an async method decorated with @handler.
#
# Handler signature contract:
# - First parameter is the typed input to this node (here: text: str)
# - Second parameter is a WorkflowContext[T], where T is the type of data this
#   node will emit via ctx.send_message (here: T is str)
#
# Within a handler you typically:
# - Compute a result
# - Forward that result to downstream node(s) using ctx.send_message(result)
class UpperCase(Executor):
    def __init__(self, id: str | None = None):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert the input to uppercase and forward it to the next node.

        Note: The WorkflowContext is parameterized with the type this handler will
        emit. Here WorkflowContext[str] means downstream nodes should expect str.
        """
        result = text.upper()

        # Send the result to the next executor in the workflow.
        await ctx.send_message(result)


# Example 2: A standalone function-based executor
# -----------------------------------------------
#
# For simple steps you can skip subclassing and define an async function with the
# same signature pattern (typed input + WorkflowContext[T]) and decorate it with
# @executor. This creates a fully functional node that can be wired into a flow.
@executor(id="reverse_text_executor")
async def reverse_text(text: str, ctx: WorkflowContext[str]) -> None:
    """Reverse the input string and signal workflow completion.

    This node emits a terminal event using ctx.add_event(WorkflowCompletedEvent).
    The data carried by the WorkflowCompletedEvent becomes the final result of
    the workflow (returned by workflow.run(...)).
    """
    result = text[::-1]

    # Send the result with a workflow completion event.
    await ctx.add_event(WorkflowCompletedEvent(result))


async def main():
    """Build and run a simple 2-step workflow using the fluent builder API."""

    upper_case = UpperCase(id="upper_case_executor")

    # Build the workflow using a fluent pattern:
    # 1) add_edge(from_node, to_node) defines a directed edge upper_case -> reverse_text
    # 2) set_start_executor(node) declares the entry point
    # 3) build() finalizes and returns an immutable Workflow object
    workflow = WorkflowBuilder().add_edge(upper_case, reverse_text).set_start_executor(upper_case).build()

    # Run the workflow by sending the initial message to the start node.
    # The run(...) call returns an event collection; its get_completed_event()
    # provides the WorkflowCompletedEvent emitted by the terminal node.
    events = await workflow.run("hello world")
    print(events.get_completed_event())

    """
    Sample Output:

    WorkflowCompletedEvent(data=DLROW OLLEH)
    """
```

#### 2. Agents in a Workflow streaming
```python
from agent_framework import ChatAgent, ChatMessage
from agent_framework.azure import AzureChatClient
from agent_framework.workflow import Executor, WorkflowBuilder, WorkflowCompletedEvent, WorkflowContext, handler
from azure.identity import AzureCliCredential

"""
Agents in a workflow with streaming

A Writer agent generates content,
then passes the conversation to a Reviewer agent that finalizes the result.
The workflow is invoked with run_stream so you can observe events as they occur.

Purpose:
Show how to wrap chat agents created by AzureChatClient inside workflow executors, wire them with WorkflowBuilder,
and consume streaming events from the workflow. Demonstrate the @handler pattern with typed inputs and typed
WorkflowContext[T] outputs, and finish by emitting a WorkflowCompletedEvent from the terminal node while printing
intermediate events for observability.
"""


class Writer(Executor):
    """Custom executor that owns a domain specific agent for content generation.

    This class demonstrates:
    - Attaching a ChatAgent to an Executor so it participates as a node in a workflow.
    - Using a @handler method to accept a typed input and forward a typed output via ctx.send_message.
    """

    agent: ChatAgent

    def __init__(self, chat_client: AzureChatClient, id: str = "writer"):
        # Create a domain specific agent using your configured AzureChatClient.
        agent = chat_client.create_agent(
            instructions=(
                "You are an excellent content writer. You create new content and edit contents based on the feedback."
            ),
        )
        # Associate this agent with the executor node. The base Executor stores it on self.agent.
        super().__init__(agent=agent, id=id)

    @handler
    async def handle(self, message: ChatMessage, ctx: WorkflowContext[list[ChatMessage]]) -> None:
        """Generate content and forward the updated conversation.

        Contract for this handler:
        - message is the inbound user ChatMessage.
        - ctx is a WorkflowContext that expects a list[ChatMessage] to be sent downstream.

        Pattern shown here:
        1) Seed the conversation with the inbound message.
        2) Run the attached agent to produce assistant messages.
        3) Forward the cumulative messages to the next executor with ctx.send_message.
        """
        # Start the conversation with the incoming user message.
        messages: list[ChatMessage] = [message]
        # Run the agent and extend the conversation with the agent's messages.
        response = await self.agent.run(messages)
        messages.extend(response.messages)
        # Forward the accumulated messages to the next executor in the workflow.
        await ctx.send_message(messages)


class Reviewer(Executor):
    """Custom executor that owns a review agent and completes the workflow."""

    agent: ChatAgent

    def __init__(self, chat_client: AzureChatClient, id: str = "reviewer"):
        # Create a domain specific agent that evaluates and refines content.
        agent = chat_client.create_agent(
            instructions=(
                "You are an excellent content reviewer. You review the content and provide feedback to the writer."
            ),
        )
        super().__init__(agent=agent, id=id)

    @handler
    async def handle(self, messages: list[ChatMessage], ctx: WorkflowContext[str]) -> None:
        """Review the full conversation transcript and complete with a final string.

        This node consumes all messages so far. It uses its agent to produce the final text,
        then signals completion by adding a WorkflowCompletedEvent to the event stream.
        """
        response = await self.agent.run(messages)
        await ctx.add_event(WorkflowCompletedEvent(response.text))


async def main():
    """Build the two node workflow and run it with streaming to observe events."""
    # Create the Azure chat client. AzureCliCredential uses your current az login.
    chat_client = AzureChatClient(credential=AzureCliCredential())
    # Instantiate the two agent backed executors.
    writer = Writer(chat_client)
    reviewer = Reviewer(chat_client)

    # Build the workflow using the fluent builder.
    # Set the start node and connect an edge from writer to reviewer.
    workflow = WorkflowBuilder().set_start_executor(writer).add_edge(writer, reviewer).build()

    # Run the workflow with the user's initial message and stream events as they occur.
    # Events include executor invoke and completion, as well as the terminal WorkflowCompletedEvent.
    completion_event = None
    async for event in workflow.run_stream(
        ChatMessage(role="user", text="Create a slogan for a new electric SUV that is affordable and fun to drive.")
    ):
        # You will see executor invoke and completion events, and then the final WorkflowCompletedEvent.
        print(event)
        if isinstance(event, WorkflowCompletedEvent):
            # The WorkflowCompletedEvent contains the final result.
            completion_event = event

    # Print the final result after the streaming loop concludes.
    if completion_event:
        print(f"Workflow completed with result: {completion_event.data}")

    """
    Sample Output:

    ExecutorInvokeEvent(executor_id=writer)
    ExecutorCompletedEvent(executor_id=writer)
    ExecutorInvokeEvent(executor_id=reviewer)
    WorkflowCompletedEvent(data=Drive the Future. Affordable Adventure, Electrified.)
    ExecutorCompletedEvent(executor_id=reviewer)
    Workflow completed with result: ...
    """
```
