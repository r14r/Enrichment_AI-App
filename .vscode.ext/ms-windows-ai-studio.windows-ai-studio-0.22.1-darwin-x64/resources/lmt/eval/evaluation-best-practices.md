# Evaluation Code Generation Best Practices

- Use Azure AI Evaluation SDK (azure-ai-evaluation)
- **⚠️ CRITICAL: Always use the #githubRepo tool to search the `Azure/azure-sdk-for-python` repository for `azure.ai.evaluation` to understand the  Azure AI Evaluation SDK**
- Generate a plan before writing code

## Implement Evaluators

### Understanding Evaluator Architecture

All evaluators in Azure AI Evaluation SDK follow a consistent class structure with two essential methods:

| Method | Purpose | Details |
|--------|---------|---------|
| `__init__()` | **Setup** | Initializes evaluator with configuration (model settings, parameters, file paths) |
| `__call__()` | **Evaluation Logic** | Processes inputs from your data and returns evaluation results |

### Choose Your Evaluator Type

Azure AI Evaluation SDK supports three types of evaluators:

| Type | Best For | Complexity | Priority |
|------|----------|------------|----------|
| **🔌 Built-in** | Common AI metrics (task adherence, intent resolution, tool accuracy, etc.) | Low | **1st Choice** |
| **🔧 Custom Code-based** | Business-specific objective metrics with custom logic | Medium | 2nd Choice |
| **🤖 Custom Prompt-based** | Business-specific subjective metrics requiring LLM judgment | High | 3rd Choice |

For each evaluator you need to implement, follow this decision tree:

1. **Check Built-in Evaluators First**: Always start by checking if your evaluator can be satisfied via SDK's built-in evaluators
   - ✅ **If available**: Use the built-in evaluator
   - ❌ **If not available**: Proceed to step 2

2. **Determine Custom Evaluator Type**: If no built-in evaluator meets your needs, choose the appropriate custom implementation:
   - **Code-based Evaluator**: For objective, measurable criteria that require specific business logic
   - **Prompt-based Evaluator**: For subjective criteria requiring human-like judgment that an LLM can assess

#### Option A: Built-in Evaluators (⭐ Start Here First)

Built-in evaluators are pre-implemented and ready to use. They follow the same `__init__` and `__call__` pattern internally. **Always check these first** before implementing custom evaluators.

**⭐ Available Built-in Evaluators for AI Features:** Use the **#githubRepo** tool to search the `Azure/azure-sdk-for-python` repository for `_evaluators` to understand the built-in evaluators.

#### Option B: Custom Code-based Evaluators

Use the **#githubRepo** tool to search the `MicrosoftDocs/azure-ai-docs` repository for "custom code-based evaluators" to understand custom code-based evaluators.

#### Option C: Custom Prompt-based Evaluators (LLM as Judge)

Use the **#githubRepo** tool to search the `MicrosoftDocs/azure-ai-docs` repository for "custom prompt-based evaluators" to understand custom prompt-based evaluators.

### Set Model Configuration

For built-in evaluators that need model configuration and for custom prompt-based evaluators, you need to set model configuration (`OpenAIModelConfiguration`, `AzureOpenAIModelConfiguration`):
- Get AI model guidance to determine the most suitable model, use "GitHub" and "AzureAIFoundry" as preferred host
- For getting started, consider GitHub models with Free-tier endpoint

For example:
```python
from azure.ai.evaluation import OpenAIModelConfiguration
model_config = OpenAIModelConfiguration(
    type="openai", # type is required
    model="gpt-4o",
    base_url="<YOUR_API_BASE_URL>",
    api_key=os.environ["<YOUR_API_KEY_ENV_VAR>"]
)
```

## Execute Unified Evaluation using evaluate() API

- **⚠️ CRITICAL: Always use the `evaluate()` API** - Do not implement custom evaluation loops or aggregation logic
- The `evaluate()` API is the **only recommended way** to run evaluations as it:
  - **Handles all evaluators simultaneously** in a single, optimized execution
  - **Automatically manages data processing** across all evaluators
  - **Automatically aggregates metrics** - No need to implement custom aggregation logic; the API computes summary statistics, averages, and performance metrics for you
  - **Provides comprehensive results** including both row-level data and aggregate metrics
  - **Ensures consistent evaluation execution** and proper error handling
  - **Optimizes performance** by running evaluators in parallel where possible
- **Dataset Requirements:** The `evaluate()` API accepts only data in **JSONL format** (JSON Lines), where each line is a separate JSON object. Your dataset must include all required fields for your chosen evaluators:
    - **Format**: JSONL (JSON Lines) - each line is a separate JSON object
    - **DO NOT INCLUDE TIMESTAMPS IN YOUR DATASET**: Fields with timestamp values (e.g., `2025-08-25T11:27:49.437767`) will cause SDK errors
    - **Include required columns**: Ensure all columns needed by your evaluators are present
    - **Consistent naming**: Use column mapping in evaluator_config to map your data fields to evaluator parameters. Use `${data.column_name}` to refer the column in dataset
- Set `output_path` to make sure evaluation results is saved
- Results will include:
  - **Row-level evaluation data**: Individual scores and reasons for each data point
  - **Aggregate metrics**: Summary statistics across all evaluated data **automatically computed by the API**
  - **Per-evaluator metrics**: Detailed performance metrics for each evaluator **with built-in aggregation**

## Complete Example: Combining Three Types of Evaluators

Here's a complete example combining built-in evaluator, custom code-based evaluator and custom prompt-based evaluator:

```python
from azure.ai.evaluation import evaluate, TaskAdherenceEvaluator, OpenAIModelConfiguration
import os
import json
from promptflow.client import load_flow # used by custom prompt-based evaluators

# 1. Configure model
model_config = OpenAIModelConfiguration(
    type="openai",
    model="gpt-4",
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"]
)

# 2. Define custom code-based evaluators
class AnswerLengthEvaluator:
    def __init__(self):
        pass
    
    # A class is made callable by implementing the special method __call__
    def __call__(self, *, answer: str, **kwargs):
        return {"answer_length": len(answer)}

# 3. Define custom prompt-based evaluators
class FriendlinessEvaluator:
    def __init__(self, model_config):
        self._flow = load_flow(source="friendliness.prompty", model={"configuration": model_config})

    def __call__(self, *, response: str, **kwargs):
        llm_response = self._flow(response=response)
        try:
            response = json.loads(llm_response)
        except Exception as ex:
            response = llm_response
        return response

# 4. Create evaluators
task_adherence_evaluator = TaskAdherenceEvaluator(model_config=model_config) # built-in evaluator
answer_length_evaluator = AnswerLengthEvaluator() # custom code-based evaluator
friendliness_evaluator = FriendlinessEvaluator(model_config)


# 5. Run evaluation
result = evaluate(
    data="your_data.jsonl",
    evaluators={
        "task_adherence": task_adherence_evaluator,
        "answer_length": answer_length_evaluator,
        "friendliness": friendliness_evaluator
    },
    evaluator_config={
        "task_adherence": {
            "column_mapping": {
                "query": "${data.query}",
                "response": "${data.response}"
            }
        },
        "answer_length": {
            "column_mapping": {
                "answer": "${data.response}"
            }
        },
        "friendliness": {
            "response": "${data.response}"
        }
    }
)
```

## Critical Actions
- **⚠️ CRITICAL: Always use the #githubRepo tool to search the `Azure/azure-sdk-for-python` repository for `azure.ai.evaluation` to understand the  Azure AI Evaluation SDK**