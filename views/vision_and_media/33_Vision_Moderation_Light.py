import base64
import json

import requests
import streamlit as st
from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="Vision Moderation Light", page_icon="🛡️")
OLLAMA = "http://localhost:11434"
st.title("🛡️ Vision Moderation (Hinweise)")


def vis_models():
    try:
        ms = [
            m["model"]
            for m in requests.get(f"{OLLAMA}/api/tags", timeout=3)
            .json()
            .get("models", [])
        ]
        ms = [
            m
            for m in ms
            if any(k in m.lower() for k in ["vision", "llava", "bakllava"])
        ] or ["llama3.2-vision", "llava:13b"]
        return ms
    except Exception:
        return ["llama3.2-vision", "llava:13b"]


model = st.selectbox("Vision-Modell", vis_models())
img = st.file_uploader("Bild", type=["png", "jpg", "jpeg", "webp"])
if st.button("Prüfen", disabled=not img):
    st.image(img)
    b64 = base64.b64encode(img.getvalue()).decode()
    prompt = "Analysiere das Bild auf sensible Inhalte (Gewalt, NSFW, persönliche Daten). Gib nur Hinweise/Tags, kein Urteil."
    data = {"model": model, "prompt": prompt, "images": [b64], "stream": True}
    box, acc = st.empty(), ""
    with requests.post(f"{OLLAMA}/api/generate", json=data, stream=True) as r:
        for ln in r.iter_lines():
            if not ln:
                continue
            acc += json.loads(ln.decode()).get("response", "")
            box.markdown(acc)
