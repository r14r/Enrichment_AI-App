"""Vision moderation helper mini app."""

from __future__ import annotations

import base64
import json

import requests
import streamlit as st

from lib.helper_streamlit import models

st.set_page_config(page_title="Vision Moderation Light", page_icon="🛡️")
st.title("🛡️ Vision Moderation (Hinweise)")


def _vision_models_only() -> list[str]:
    available = models()
    filtered = [
        name
        for name in available
        if any(keyword in name.lower() for keyword in ("vision", "llava", "bakllava"))
    ]
    return filtered or ["llama3.2-vision", "llava:13b"]


selected_model = st.selectbox("Vision-Modell", _vision_models_only())
image_file = st.file_uploader("Bild", type=["png", "jpg", "jpeg", "webp"])

if st.button("Prüfen", disabled=not image_file):
    assert image_file is not None
    st.image(image_file)
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
    with requests.post("http://localhost:11434/api/generate", json=payload, stream=True) as response:
        for line in response.iter_lines():
            if not line:
                continue
            acc += json.loads(line.decode()).get("response", "")
            placeholder.markdown(acc)
