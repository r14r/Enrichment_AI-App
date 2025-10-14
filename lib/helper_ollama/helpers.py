# Add lib directory to path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ollama_utils'))

from lib.helper_ollama import get_local_llms


def get_chat_models() -> list[str]:
    """Get list of chat model names for Streamlit selectbox."""
    try:
        models = get_local_llms("chat")
        return [model["name"] for model in models]
    except Exception:
        return ["llama3.2", "mistral:7b"]


def get_vision_models() -> list[str]:
    """Get list of vision-capable model names for Streamlit selectbox."""
    try:
        models = get_local_llms("vision")
        return [model["name"] for model in models]
    except Exception:
        return ["llama3.2-vision", "llava"]


def get_embedding_models() -> list[str]:
    """Get list of embedding model names for Streamlit selectbox."""
    try:
        models = get_local_llms("embedding")
        return [model["name"] for model in models]
    except Exception:
        return ["nomic-embed-text"]


def get_tool_models() -> list[str]:
    """Get list of tool/function calling model names for Streamlit selectbox."""
    try:
        models = get_local_llms("tools")
        return [model["name"] for model in models]
    except Exception:
        return ["llama3.1", "mistral"]


def get_thinking_models() -> list[str]:
    """Get list of thinking/reasoning model names for Streamlit selectbox."""
    try:
        models = get_local_llms("thinking")
        return [model["name"] for model in models]
    except Exception:
        return ["deepseek-r1", "llama3.2"]


def get_all_models() -> list[str]:
    """Get list of all model names for Streamlit selectbox."""
    try:
        models = get_local_llms()
        return [model["name"] for model in models]
    except Exception:
        return ["llama3.2", "mistral:7b"]


def get_best_model_for_function(func: str) -> str:
    """Get the best model name for a specific function."""
    try:
        models = get_local_llms(func)
        if models:
            # Return the first model (could be enhanced with better selection logic)
            return models[0]["name"]
    except Exception:
        pass

    # Fallback defaults
    defaults = {
        "chat": "llama3.2",
        "vision": "llama3.2-vision",
        "embedding": "nomic-embed-text",
        "tools": "llama3.1",
        "thinking": "deepseek-r1",
    }
    return defaults.get(func, "llama3.2")


def get_model_capabilities(model_name: str) -> list[str]:
    """Get capabilities of a specific model by name."""
    try:
        all_models = get_local_llms()
        for model in all_models:
            if model["name"] == model_name:
                return model["capabilities"]
    except Exception:
        pass
    return []
