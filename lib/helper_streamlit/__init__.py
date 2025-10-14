"""Reusable Streamlit helpers for interacting with the Ollama API."""

from __future__ import annotations

import json
from typing import Iterable, List

import requests
import streamlit as st

from lib.helper_ollama import OLLAMA


def _extract_model_names(models_payload: Iterable[dict]) -> List[str]:
    """Return sorted model names from an Ollama tag payload."""

    names = sorted({str(model.get("model", "")).strip() for model in models_payload})
    return [name for name in names if name]


def models() -> List[str]:
    """Fetch available Ollama models with sensible fallbacks.

    When the Ollama server cannot be reached we keep the UX intact by returning a
    set of commonly available models.
    """

    try:
        response = requests.get(f"{OLLAMA}/api/tags", timeout=3)
        response.raise_for_status()
        payload = response.json().get("models", [])
        names = _extract_model_names(payload)
        return names or ["llama3.2", "mistral:7b"]
    except Exception:  # noqa: BLE001 - best effort fallback for UI friendliness
        return ["llama3.2", "mistral:7b"]


def generate(model: str, prompt: str) -> str:
    """Stream responses from Ollama into the UI and return the final text."""

    box, acc = st.empty(), ""

    with requests.post(
        f"{OLLAMA}/api/generate",
        json={"model": model, "prompt": prompt, "stream": True},
        stream=True,
    ) as response:
        for ln in response.iter_lines():
            if not ln:
                continue
            part = json.loads(ln.decode("utf-8"))
            acc += part.get("response", "")
            box.markdown(acc)
    return acc


def add_select_model(label: str = "Modell") -> str:
    """Render a model selectbox with the available Ollama models."""

    return st.selectbox(label, models())
