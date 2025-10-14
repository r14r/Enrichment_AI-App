"""Generate multiple content ideas for a topic."""

from __future__ import annotations

import streamlit as st

from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="Ideen-Generator x10", page_icon="💡")

st.title("💡 Ideen-Generator (x10)")
model = add_select_model()
topic = st.text_input("Thema/Branche", "SaaS für Bildung")
if st.button("Ideen erzeugen"):
    prompt = (
        "Erzeuge 10 Content-Ideen mit Titel + 1-Satz-Hook zum Thema: "
        f"{topic}. Gib als nummerierte Liste zurück."
    )
    generate(model, prompt)
