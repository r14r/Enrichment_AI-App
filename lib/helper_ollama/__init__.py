"""
Ollama LLM Discovery and Filtering Module - Cleaned Up Version

This module provides functions to discover and filter locally installed Ollama models
by function type: embedding, tools, vision, thinking, and chat.
"""

import ollama as ollama_sdk


OLLAMA = "http://localhost:11434"


def get_local_llms(func=None):
    """
    Get all locally installed LLMs that support the specified function.
    
    Args:
        func: Function/capability to filter for:
              - "embedding": Text embedding models
              - "vision": Vision/image processing models  
              - "tools": Tool/function calling models
              - "thinking": Reasoning/thinking models
              - "chat": General chat/conversation models
              - None: Returns all models with detected capabilities
    
    Returns:
        List of dictionaries containing model information including name, size, and capabilities
    
    Example:
        >>> # Get all vision models
        >>> vision_models = get_local_llms("vision")
        >>> 
        >>> # Get all embedding models
        >>> embed_models = get_local_llms("embedding")
        >>> 
        >>> # Get all models with capabilities
        >>> all_models = get_local_llms()
    """
    
    # Validate input
    valid_functions = ["embedding", "tools", "vision", "thinking", "chat"]
    if func and func not in valid_functions:
        raise ValueError(f"Invalid func: {func}. Must be one of {valid_functions} or None")
    
    try:
        # Get all installed models from Ollama using direct function
        response = ollama_sdk.list()
        all_models = response.get("models", [])
        
        # Filter models based on function
        filtered_models = []
        
        for model in all_models:
            model_name = getattr(model, 'model', '')
            model_name_lower = model_name.lower()
            
            # Detect capabilities
            capabilities = _detect_model_capabilities(model_name_lower)
            
            model_info = {
                "name": model_name,
                "size": getattr(model, 'size', 0),
                "modified_at": getattr(model, 'modified_at', ''),
                "digest": getattr(model, 'digest', ''),
                "details": getattr(model, 'details', {}),
                "capabilities": capabilities
            }
            
            # Filter by function if specified
            if func is None:
                # Return all models with their capabilities
                filtered_models.append(model_info)
            elif func in capabilities:
                # Return only models that support the specified function
                filtered_models.append(model_info)
        
        return filtered_models
        
    except Exception as e:
        raise Exception(f"Failed to connect to Ollama or process models: {e}")


def _detect_model_capabilities(model_name_lower):
    """
    Detect the capabilities of a model based on its name.
    
    Args:
        model_name_lower: Lowercase model name
        
    Returns:
        List of capabilities the model supports
    """
    capabilities = []
    
    # Check for embedding capabilities
    if _supports_embedding(model_name_lower):
        capabilities.append("embedding")
    
    # Check for vision capabilities
    if _supports_vision(model_name_lower):
        capabilities.append("vision")
    
    # Check for tool/function calling capabilities
    if _supports_tools(model_name_lower):
        capabilities.append("tools")
    
    # Check for thinking/reasoning capabilities
    if _supports_thinking(model_name_lower):
        capabilities.append("thinking")
    
    # Check for general chat capabilities (most models)
    if _supports_chat(model_name_lower):
        capabilities.append("chat")
    
    return capabilities


def _supports_embedding(model_name_lower):
    """Check if model supports text embedding."""
    embedding_indicators = [
        "embed", "embedding", "nomic-embed", "bge", "sentence", 
        "all-minilm", "e5", "gte", "multilingual-e5", "paraphrase",
        "text-embedding", "instructor", "thenlper"
    ]
    return any(indicator in model_name_lower for indicator in embedding_indicators)


def _supports_vision(model_name_lower):
    """Check if model supports vision/image processing."""
    vision_indicators = [
        "vision", "llava", "bakllava", "moondream", "cogvlm", 
        "qwen-vl", "qwen2-vl", "internvl", "minicpm-v", "yi-vl", 
        "deepseek-vl", "blip", "clip", "fuyu", "kosmos", "flamingo",
        "otter", "minigpt", "instructblip", "lynx", "idefics"
    ]
    return any(indicator in model_name_lower for indicator in vision_indicators)


def _supports_tools(model_name_lower):
    """Check if model supports tool/function calling."""
    # Tool calling models often have specific naming or are known capable models
    tool_indicators = [
        "function", "tool", "agent", "hermes", "mixtral", "command",
        "gorilla", "toolformer", "react", "planning"
    ]
    
    # Known models that support function calling
    known_tool_models = [
        "llama3", "llama3.1", "llama3.2", "mistral", "mixtral", 
        "qwen", "yi", "deepseek", "phi"
    ]
    
    return (any(indicator in model_name_lower for indicator in tool_indicators) or
            any(known in model_name_lower for known in known_tool_models))


def _supports_thinking(model_name_lower):
    """Check if model supports reasoning/thinking capabilities."""
    thinking_indicators = [
        "reasoning", "thinking", "o1", "r1", "chain", "cot", 
        "reason", "logic", "math", "solver", "step", "thought"
    ]
    
    # Known thinking/reasoning models
    known_thinking_models = [
        "deepseek-r1", "qwen-reasoning", "o1", "reasoning"
    ]
    
    return (any(indicator in model_name_lower for indicator in thinking_indicators) or
            any(known in model_name_lower for known in known_thinking_models))


def _supports_chat(model_name_lower):
    """Check if model supports general chat/conversation."""
    # Most models support chat unless they're specialized
    specialized_only = ["embed", "embedding", "bge", "sentence", "nomic-embed"]
    
    # If it's a specialized embedding model, it doesn't support chat
    if any(indicator in model_name_lower for indicator in specialized_only):
        return False
    
    # General chat indicators (most language models)
    chat_indicators = [
        "llama", "mistral", "codellama", "dolphin", "orca", "vicuna", 
        "alpaca", "wizard", "openchat", "neural", "chat", "instruct",
        "qwen", "yi", "deepseek", "phi", "gemma", "solar", "claude",
        "gpt", "falcon", "mpt", "bloom", "opt", "pythia", "stablelm"
    ]
    
    return any(indicator in model_name_lower for indicator in chat_indicators)


def get_model_info(model_name):
    """Get detailed information about a specific model."""
    try:
        response = ollama_sdk.show(model_name)
        
        # Add capability detection
        capabilities = _detect_model_capabilities(model_name.lower())
        
        # Create enhanced response
        enhanced_response = {
            "name": model_name,
            "capabilities": capabilities,
            "details": getattr(response, 'details', {}),
            "modelfile": getattr(response, 'modelfile', ''),
            "parameters": getattr(response, 'parameters', ''),
            "template": getattr(response, 'template', ''),
            "system": getattr(response, 'system', ''),
        }
        
        return enhanced_response
        
    except Exception as e:
        raise Exception(f"Failed to get model info for {model_name}: {e}")


def list_models_by_capability():
    """Get models organized by capability."""
    try:
        all_models = get_local_llms()
        
        categorized = {
            "embedding": [],
            "vision": [],
            "tools": [],
            "thinking": [],
            "chat": []
        }
        
        for model in all_models:
            for capability in model["capabilities"]:
                if capability in categorized:
                    categorized[capability].append(model)
        
        # Add summary
        categorized["summary"] = {
            "total_models": len(all_models),
            "embedding_count": len(categorized["embedding"]),
            "vision_count": len(categorized["vision"]),
            "tools_count": len(categorized["tools"]),
            "thinking_count": len(categorized["thinking"]),
            "chat_count": len(categorized["chat"])
        }
        
        return categorized
        
    except Exception as e:
        return {
            "error": str(e),
            "embedding": [],
            "vision": [],
            "tools": [],
            "thinking": [],
            "chat": [],
            "summary": {"total_models": 0}
        }


def generate(model_name, prompt, stream=False, **kwargs):
    """Generate text using a specific model."""
    try:
        response = ollama_sdk.generate(
            model=model_name,
            prompt=prompt,
            stream=stream,
            **kwargs
        )
        return response
    except Exception as e:
        raise Exception(f"Failed to generate with {model_name}: {e}")


def chat(model_name, messages, stream=False, **kwargs):
    """Chat with a model."""
    try:
        response = ollama_sdk.chat(
            model=model_name,
            messages=messages,
            stream=stream,
            **kwargs
        )
        return response
    except Exception as e:
        raise Exception(f"Failed to chat with {model_name}: {e}")


def embeddings(model_name, text, **kwargs):
    """Generate embeddings using an embedding model."""
    try:
        response = ollama_sdk.embeddings(
            model=model_name,
            prompt=text,
            **kwargs
        )
        return response
    except Exception as e:
        raise Exception(f"Failed to generate embeddings with {model_name}: {e}")


# Export main functions
__all__ = [
    "get_local_llms",
    "get_model_info",
    "list_models_by_capability",
    "generate",
    "chat",
    "embeddings"
]
