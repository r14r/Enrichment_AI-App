import base64
import json

import requests
import streamlit as st
from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="Mini Vision Analyzer", page_icon="🖼️")
OLLAMA = "http://localhost:11434"

st.title("🖼️ Mini Vision Analyzer")


# Versuch, ein Vision-Modell als Default zu wählen
def get_vison_model(ms):
    for i, m in enumerate(ms):
        if any(k in m.lower() for k in ["vision", "llava", "bakllava"]):
            return i

    return 0


# --- Model wählen --------------------------------------------------------------------------------
try:
    models = [
        m["model"]
        for m in requests.get(f"{OLLAMA}/api/tags", timeout=10).json().get("models", [])
    ]
except Exception:
    models = ["llama3.2", "mistral:7b"]

# --- Sidebar -------------------------------------------------------------------------------------
with st.sidebar:
    model = st.selectbox("Vision-Modell", models, index=get_vison_model(models))


prompt = st.text_input(
    "Analyse-Prompt", "Beschreibe den Bildinhalt präzise und stichpunktartig."
)
img = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg", "webp"])
go = st.button("🔍 Analysieren (Streaming)")
box = st.empty()

if go and img:
    st.image(img, caption=img.name)
    b64 = base64.b64encode(img.getvalue()).decode("utf-8")
    data = {"model": model, "prompt": prompt, "images": [b64], "stream": True}

    with requests.post(f"{OLLAMA}/api/generate", json=data, stream=True) as r:
        text = ""
        for line in r.iter_lines():
            if not line:
                continue
            part = json.loads(line.decode("utf-8"))
            text += part.get("response", "")
            box.markdown(text)  # Live-Update
        st.download_button(
            "⬇️ Ergebnis speichern", text.encode("utf-8"), f"analysis_{img.name}.txt"
        )
