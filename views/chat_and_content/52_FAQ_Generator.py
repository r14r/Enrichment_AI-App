import json

import requests
import streamlit as st
from lib.helper_streamlit import add_select_model, generate

OLLAMA = "http://localhost:11434"
st.set_page_config(page_title="FAQ Generator", page_icon="❓")


def models():
    try:
        return [
            m["model"]
            for m in requests.get(f"{OLLAMA}/api/tags", timeout=3)
            .json()
            .get("models", [])
        ] or ["llama3.2", "mistral:7b"]
    except Exception:
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


st.title("❓ FAQ Generator")
model = add_select_model()
src = st.text_area(
    "Quelltext/Inhalt", "Unsere Plattform analysiert medizinische Bilder ..."
)
if st.button("FAQ erstellen"):
    p = (
        "Erzeuge 10 FAQ-Fragen mit kurzen, klaren Antworten basierend auf diesem Inhalt (Deutsch):\n\n"
        + src
    )
    generate(model, p)
