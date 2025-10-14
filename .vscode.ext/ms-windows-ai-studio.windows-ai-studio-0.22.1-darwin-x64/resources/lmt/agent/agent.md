# Agent Code Generation Best Practices

- Generate a plan before writing code
- Explain why you selects the model
- Explain why you selects the SDK

## 1. AI Model
- Get AI model guidance to determine the most suitable model, use "GitHub" and "AzureAIFoundry" as preferred host
- For getting started, single agent, or simple chat app, consider GitHub models with Free-tier endpoint
- For multi-agents, complex workflow, or production app, consider Azure AI Foundry models

## 2. SDK
- Use **Microsoft Agent Framework** for agent app, with following highlights
  - Flexible Agent Framework: build, orchestrate, and deploy AI agents and multi-agent systems
  - Multi-Agent Orchestration: Group chat, sequential, concurrent, and handoff patterns
  - Plugin Ecosystem: Extend with native functions, OpenAPI, Model Context Protocol (MCP), and more
  - LLM Support: OpenAI, Azure OpenAI, Azure AI Foundry, and more
  - Runtime Support: In-process and distributed agent execution
  - Multimodal: Text, vision, and function calling
  - Cross-Platform: .NET and Python implementations

### Installation
For how to install the agent-framework package from the GitHub repo in a virtual environment, please follow these steps:
- Create a requirements.txt and constraints.txt
- Create and activate a virtual environment
- Install the main package with extras from the repo using pip or uv
- Verify the installation

Quick summary:
- Minimum Python: >= 3.10 (project requires-python = ">=3.10").
- GitHub repository: https://github.com/microsoft/agent-framework.
- Package subdirectories used by pip:
	- Main package: `python/packages/main`
	- Azure: `python/packages/azure`
	- Foundry: `python/packages/foundry`
	- Workflow: `python/packages/workflow`

For example, when you want to use Agent Framework with Azure OpenAI clients, use a requirements.txt like this:
```
agent-framework[azure] @ git+https://github.com/microsoft/agent-framework.git@main#subdirectory=python/packages/main
```

with constraints for the extras, in constraints.txt:

```
agent-framework-azure @ git+https://github.com/microsoft/agent-framework.git@main#subdirectory=python/packages/azure
agent-framework-foundry @ git+https://github.com/microsoft/agent-framework.git@main#subdirectory=python/packages/foundry
agent-framework-workflow @ git+https://github.com/microsoft/agent-framework.git@main#subdirectory=python/packages/workflow
```

Then install with:

```bash
pip install -r requirements.txt --constraint constraints.txt
```

## 3. Code Samples
- Get Agent & Model Code Sample to get detailed code samples and snippets
- Can get multiple times for different intents or user changes opinion

## 4. (OPTIONAL) Resource Preparation
- **Do this if using Azure AI Foundry project / model but user currently does not have one.**
- This requires user already has **Azure AI Foundry** project / model deployed.
- Call VSCode Command \`workbench.view.extension.azure-ai-foundry\` to navigate user to Azure AI Foundry Extension for resource management.
