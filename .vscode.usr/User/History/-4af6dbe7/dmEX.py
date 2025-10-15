"""CSV question answering mini-app."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="CSV Q&A", page_icon="📊")

st.title("📊 CSV Q&A")
model = add_select_model()
upload = st.file_uploader("CSV hochladen", type=["csv"])
question = st.text_input(
    "Frage an die Tabelle", "Welche 3 wichtigsten Erkenntnisse?"
)

dataframe = None
if upload:
    dataframe = pd.read_csv(upload)
    st.dataframe(dataframe.head(15), width='stretch')

if st.button("Analysieren", disabled=dataframe is None):
    assert dataframe is not None  # for type checkers
    prompt = (
        "Antworte stichpunktartig basierend auf dieser CSV (Kopf, Spalten, Statistik):\n"
        f"Spalten: {list(dataframe.columns)}\n"
        f"Shape: {dataframe.shape}\n"
        f"Kopf:\n{dataframe.head(10).to_csv(index=False)}\n\n"
        f"Frage: {question}"
    )
    generate(model, prompt)
