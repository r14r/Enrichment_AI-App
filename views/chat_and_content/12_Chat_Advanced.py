import json

import requests
import streamlit as st
from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="MiniApp: Chat", page_icon="🧠")

OLLAMA = "http://localhost:11434"

st.title("🧠 Mini Ollama")

# --- Model wählen --------------------------------------------------------------------------------
try:
    models = [
        m["model"] for m in requests.get(f"{OLLAMA}/api/tags").json().get("models", [])
    ]
except Exception:
    models = ["llama3.2", "mistral:7b"]

# --- Sidebar -------------------------------------------------------------------------------------
with st.sidebar:
    model = st.selectbox("Modell wählen", models)

# --- Prompt eingeben -----------------------------------------------------------------------------
prompt = st.text_area("Prompt", height=160, placeholder="Schreibe hier deinen Prompt …")

go = st.button("🚀 Abfragen")
box = st.empty()

if go and prompt.strip():
    url = f"{OLLAMA}/api/generate"
    data = {"model": model, "prompt": prompt, "stream": True}

    with st.spinner("Wird generiert …"):
        res, acc = requests.post(url, json=data, stream=True), ""

        for line in res.iter_lines():
            if not line:
                continue

            chunk = json.loads(line.decode("utf-8"))
            acc += chunk.get("response", "")
            box.markdown(acc)  # Live-Update

    if chunk.get("done"):
        st.success("Fertig.")
