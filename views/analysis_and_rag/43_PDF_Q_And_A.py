"""PDF question answering mini-app."""

from __future__ import annotations

import io

import streamlit as st

from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="PDF Q&A", page_icon="📄")

st.title("📄 PDF Q&A")
model = add_select_model()
upload = st.file_uploader("PDF hochladen", type=["pdf"])
question = st.text_input("Frage", "Fasse die Kernaussagen zusammen.")

def read_pdf(file_handle) -> str:
    """Return extracted text from a PDF file handle."""

    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(file_handle.read()))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        from pdfminer.high_level import extract_text

        file_handle.seek(0)
        return extract_text(file_handle)


extracted_text = ""
if upload:
    extracted_text = read_pdf(upload)
    st.code(extracted_text[:1200] or "—")

if st.button("Analysieren", disabled=not extracted_text.strip()):
    prompt = (
        "Analysiere folgenden PDF-Text (gekürzt) und beantworte: "
        f"{question}. Antworte strukturiert auf Deutsch.\n\n"
        f"{extracted_text[:12000]}"
    )
    generate(model, prompt)
