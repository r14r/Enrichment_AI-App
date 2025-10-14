import requests
import json

import streamlit as st

from lib.helper_ollama import OLLAMA

def models():
    try:
        return [
            m["model"]
            for m in requests.get(f"{OLLAMA}/api/tags", timeout=3)
            .json()
            .get("models", [])
        ] or ["llama3.2", "mistral:7b"]
    except Exception as e:
        return ["llama3.2", "mistral:7b"]


def generate(model, prompt):
    box, acc = st.empty(), ""
    
    with requests.post(
        f"{OLLAMA}/api/generate",
        json={"model": model, "prompt": prompt, "stream": True},
        stream=True,
    ) as r:
        for ln in r.iter_lines():
            if not ln:
                continue
            part = json.loads(ln.decode("utf-8"))
            acc += part.get("response", "")
            box.markdown(acc)
    return acc

def add_select_model():
    return st.selectbox("Modell", models())