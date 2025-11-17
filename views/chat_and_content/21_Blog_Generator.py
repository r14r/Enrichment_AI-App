import streamlit as st
from lib.helper_streamlit import add_select_model, generate


st.set_page_config(page_title="Blog Generator", page_icon="📝")


st.title("📝 Blog Generator")
model = add_select_model()
topic = st.text_input("Thema", "Die Zukunft der KI")
tone = st.selectbox("Ton", ["Neutral", "Professionell", "Locker", "Inspirierend"], 1)
length = st.slider("Ziel-Länge (Wörter)", 200, 2000, 800, 50)

if st.button("Generieren"):
    p = f"Schreibe einen {tone.lower()}en Blogartikel (~{length} Wörter) über: {topic}. Markdown, H1/H2, Bulletpoints, Fazit."
    txt = generate(model, p)
    st.download_button("⬇️ Markdown", txt.encode(), f"blog_{topic.replace(' ', '_')}.md")
