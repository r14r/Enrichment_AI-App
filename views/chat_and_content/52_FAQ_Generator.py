"""Generate FAQs from a content block."""

from __future__ import annotations

import streamlit as st

from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="FAQ Generator", page_icon="❓")

st.title("❓ FAQ Generator")
model = add_select_model()
source_text = st.text_area(
    "Quelltext/Inhalt", "Unsere Plattform analysiert medizinische Bilder ..."
)

if st.button("FAQ erstellen"):
    prompt = (
        "Erzeuge 10 FAQ-Fragen mit kurzen, klaren Antworten basierend auf diesem Inhalt (Deutsch):\n\n"
        + source_text
    )
    generate(model, prompt)
