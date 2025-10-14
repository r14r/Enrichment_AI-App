import glob
import os

import streamlit as st
from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="RAG Folder Loader (Lite)", page_icon="🗂️")


st.title("🗂️ RAG: Ordner-Loader (Lite)")
model = add_select_model()

folder = st.text_input("Ordner mit .txt/.md", "./docs")
query = st.text_input("Frage", "Worum geht es insgesamt?")

if st.button("Antwort finden"):
    texts = []
    for pth in glob.glob(os.path.join(folder, "**", "*.*"), recursive=True):
        if pth.lower().endswith((".txt", ".md")):
            try:
                texts.append(
                    open(pth, "r", encoding="utf-8", errors="ignore").read()[:4000]
                )
            except Exception as e:  # noqa: F841
                pass
    context = "\n---\n".join(texts)[:20000] if texts else ""
    p = f"Beantworte die Frage auf Basis des Kontexts (Auszüge):\n{context}\n\nFrage: {query}"
    p = p if context else f"Keine Dateien gefunden. Antworte trotzdem kurz auf: {query}"

    generate(model, p)
