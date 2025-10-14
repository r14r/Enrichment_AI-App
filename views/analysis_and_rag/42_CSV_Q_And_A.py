import json

import requests
import streamlit as st
from lib.helper_streamlit import add_select_model, generate

OLLAMA = "http://localhost:11434"
st.set_page_config(page_title="CSV Q&A", page_icon="📊")


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


import pandas as pd

st.title("📊 CSV Q&A")
model = add_select_model()
up = st.file_uploader("CSV hochladen", type=["csv"])
q = st.text_input("Frage an die Tabelle", "Welche 3 wichtigsten Erkenntnisse?")
df = None
if up:
    df = pd.read_csv(up)
    st.dataframe(df.head(15), use_container_width=True)
if st.button("Analysieren", disabled=not (df is not None)):
    p = f"Antworte stichpunktartig basierend auf dieser CSV (Kopf, Spalten, Statistik):\nSpalten: {list(df.columns)}\nShape: {df.shape}\nKopf:\n{df.head(10).to_csv(index=False)}\n\nFrage: {q}"
    generate(model, p)
