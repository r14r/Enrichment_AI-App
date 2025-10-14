"""Advanced chat interface with streaming output."""

from __future__ import annotations

import streamlit as st

from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="MiniApp: Chat", page_icon="🧠")

st.title("🧠 Mini Ollama")

with st.sidebar:
    selected_model = add_select_model("Modell wählen")

prompt = st.text_area("Prompt", height=160, placeholder="Schreibe hier deinen Prompt …")
trigger = st.button("🚀 Abfragen")

if trigger and prompt.strip():
    with st.spinner("Wird generiert …"):
        result = generate(selected_model, prompt)
    if result.strip():
        st.success("Fertig.")
