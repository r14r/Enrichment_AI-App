import json

import requests
import streamlit as st
from lib.helper_streamlit import add_select_model, generate

OLLAMA = "http://localhost:11434"
st.set_page_config(page_title="PDF Q&A", page_icon="📄")


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


import io

st.title("📄 PDF Q&A")
model = add_select_model()
up = st.file_uploader("PDF hochladen", type=["pdf"])
q = st.text_input("Frage", "Fasse die Kernaussagen zusammen.")
text = ""


def read_pdf(file):
    try:
        from pypdf import PdfReader

        r = PdfReader(io.BytesIO(file.read()))
        return "\n".join(page.extract_text() or "" for page in r.pages)
    except Exception:
        from pdfminer.high_level import extract_text

        file.seek(0)
        return extract_text(file)


if up:
    text = read_pdf(up)
    st.code(text[:1200] or "—")
if st.button("Analysieren", disabled=not text.strip()):
    p = f"Analysiere folgenden PDF-Text (gekürzt) und beantworte: {q}. Antworte strukturiert auf Deutsch.\n\n{text[:12000]}"
    generate(model, p)
