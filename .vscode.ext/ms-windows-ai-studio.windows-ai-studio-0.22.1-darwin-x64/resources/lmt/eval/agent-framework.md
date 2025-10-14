#### SDK-Specific Practices

##### agent-framework SDK
The agent-framework SDK provides built-in support for capturing both final outputs and conversation histories:

- **Final Output**: Available in the `text` property of the `AgentRunResponse` object returned by `agent.run()`
- **Conversation Histories**: Available in the `messages` property of the `AgentRunResponse` object
- **Usage**: Since this SDK returns conversation histories directly, you can collect comprehensive evaluation data without requiring additional tracing infrastructure
- **Data Collection**: Extract both `response.text` (final output) and `response.messages` (conversation histories) from the `AgentRunResponse` for complete evaluation datasets

##### Understanding Key Classes

For detailed information about the agent-framework SDK's data structures, use the **#githubRepo** tool to search the `microsoft/agent-framework` repository:

- **AgentRunResponse**: Search for `AgentRunResponse` to understand the complete response structure and available properties
- **ChatMessage**: Search for `ChatMessage` to understand the message format used in conversation histories
- **Contents**: Search for `Contents` to understand how message content is structured

This will help you better understand the data format and structure when working with evaluation datasets from the agent-framework SDK.