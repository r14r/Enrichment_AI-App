import io
import json

import requests
import streamlit as st

from lib.helper_streamlit import models

st.set_page_config(page_title="Mini Data Analyzer", page_icon="📄")
st.title("📄🔍 Mini Data Analyzer (CSV & PDF)")

OLLAMA = "http://localhost:11434"

# --- Model wählen --------------------------------------------------------------------------------
available_models = models()

# --- Sidebar -------------------------------------------------------------------------------------
with st.sidebar:
    model = st.selectbox("Modell wählen", available_models)

question = st.text_input(
    "Deine Analysefrage", "Fasse die wichtigsten Erkenntnisse zusammen."
)

# Datei-Upload
up = st.file_uploader("CSV oder PDF hochladen", type=["csv", "pdf"])
preview = st.empty()
meta = {}


def _read_csv(file):
    import pandas as pd

    df = pd.read_csv(file)
    st.subheader("CSV Vorschau")
    st.dataframe(df.head(20), width='stretch')
    desc = df.describe(include="all").to_string()
    info = f"Spalten: {list(df.columns)}\nForm: {df.shape}\n\nDescribe:\n{desc}"
    return info, df


def _read_pdf(file):
    text = ""
    try:
        # 1) pypdf

        from pypdf import PdfReader

        r = PdfReader(io.BytesIO(file.read()))
        text = "\n".join(page.extract_text() or "" for page in r.pages)
    except Exception:
        # 2) pdfminer.six
        try:
            from pdfminer.high_level import extract_text

            file.seek(0)
            text = extract_text(file)
        except Exception as e:
            st.error(f"PDF konnte nicht extrahiert werden: {e}")

    return text


doc_text, df = "", None
if up:
    if up.type.endswith("csv"):
        doc_text, df = _read_csv(up)
        meta = {"kind": "csv", "name": up.name}
    else:
        text = _read_pdf(up)
        st.subheader("PDF Vorschau (erste 1200 Zeichen)")
        st.code(text[:1200] or "—")
        doc_text = text
        meta = {"kind": "pdf", "name": up.name}

# Abfrage an Ollama (Streaming)
if st.button("🚀 Analysieren", disabled=not (up and doc_text.strip())):
    st.caption(f"Frage: {question}")
    # Eingabe begrenzen, um Riesen-Dokumente handhabbar zu machen
    MAX_CHARS = 12000
    context = doc_text[:MAX_CHARS]
    sys_prompt = (
        "Du bist Daten-/Dokumentenanalyst/in. Antworte strukturiert, präzise und mit Stichpunkten, "
        "nenne ggf. Annahmen. Antworte auf Deutsch."
    )
    user_prompt = (
        f"Datei: {meta.get('name')} (Typ: {meta.get('kind')})\n\n"
        f"Kontext (gekürzt auf {len(context)} Zeichen):\n{context}\n\n"
        f"Aufgabe/Frage:\n{question}\n\n"
        "Gib klare, gegliederte Ergebnisse zurück. Wenn Zahlen vorhanden sind, baue kurze Bullet-Insights."
    )
    payload = {
        "model": model,
        "prompt": f"{sys_prompt}\n\n{user_prompt}",
        "stream": True,
    }
    box = st.empty()
    acc = ""
    try:
        with requests.post(f"{OLLAMA}/api/generate", json=payload, stream=True) as r:
            r.raise_for_status()
            for ln in r.iter_lines():
                if not ln:
                    continue
                chunk = json.loads(ln.decode("utf-8"))
                acc += chunk.get("response", "")
                box.markdown(acc)
        st.download_button(
            "⬇️ Ergebnis speichern",
            acc.encode("utf-8"),
            f"analysis_{meta.get('name', 'doc')}.md",
        )
    except Exception as e:
        st.error(f"Ollama-Fehler: {e}")
