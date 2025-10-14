"""Streamlit mini app for vision model inference."""

from __future__ import annotations

import base64
import json

import requests
import streamlit as st

from lib.helper_streamlit import models

st.set_page_config(page_title="Mini Vision Analyzer", page_icon="🖼️")

st.title("🖼️ Mini Vision Analyzer")


def _vision_model_index(available_models: list[str]) -> int:
    for index, name in enumerate(available_models):
        if any(keyword in name.lower() for keyword in ("vision", "llava", "bakllava")):
            return index
    return 0


available_models = models()
with st.sidebar:
    selected_model = st.selectbox(
        "Vision-Modell", available_models, index=_vision_model_index(available_models)
    )

prompt = st.text_input(
    "Analyse-Prompt", "Beschreibe den Bildinhalt präzise und stichpunktartig."
)
image_file = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg", "webp"])
trigger = st.button("🔍 Analysieren (Streaming)")
placeholder = st.empty()

if trigger and image_file:
    st.image(image_file, caption=image_file.name)
    encoded = base64.b64encode(image_file.getvalue()).decode("utf-8")
    payload = {
        "model": selected_model,
        "prompt": prompt,
        "images": [encoded],
        "stream": True,
    }

    with requests.post("http://localhost:11434/api/generate", json=payload, stream=True) as response:
        text = ""
        for line in response.iter_lines():
            if not line:
                continue
            part = json.loads(line.decode("utf-8"))
            text += part.get("response", "")
            placeholder.markdown(text)
        st.download_button(
            "⬇️ Ergebnis speichern", text.encode("utf-8"), f"analysis_{image_file.name}.txt"
        )
