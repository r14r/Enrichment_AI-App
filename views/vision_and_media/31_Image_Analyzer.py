"""Vision moderation helper mini app."""

from __future__ import annotations

import base64
import json

import requests
import streamlit as st

from lib.helper_ollama.helpers import get_vision_models

st.set_page_config(page_title="Bildanalyse", page_icon="🛡️")
st.title("🛡️ Bildanalyse")


selected_model = st.selectbox("Vision-Modell", get_vision_models())
image_file = st.file_uploader("Bild", type=["png", "jpg", "jpeg", "webp"])

if st.button("Prüfen", disabled=not image_file):
    encoded = base64.b64encode(image_file.getvalue()).decode()
    prompt = (
        "Analysiere das Bild auf sensible Inhalte (Gewalt, NSFW, persönliche Daten). "
        "Gib nur Hinweise/Tags, kein Urteil."
    )
    payload = {
        "model": selected_model,
        "prompt": prompt,
        "images": [encoded],
        "stream": True,
    }
    placeholder, acc = st.empty(), ""
    with requests.post(
        "http://localhost:11434/api/generate", json=payload, stream=True
    ) as response:
        for line in response.iter_lines():
            if not line:
                continue
            acc += json.loads(line.decode()).get("response", "")
            placeholder.markdown(acc)

if image_file:
    st.image(image_file, caption=image_file.name)
