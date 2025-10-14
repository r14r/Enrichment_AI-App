import streamlit as st

st.title("⚡ Enrichment MiniApps – Übersicht")

st.subheader("Willkommen bei den Enrichment MiniApps")
st.markdown(
    """
    Wähle in der Navigation eine App aus. Unter **🚀 Neue Use Cases** findest du die zehn frischen Beispiele
    dafür, wie sich Ollama und Streamlit in unterschiedlichen Bereichen einsetzen lassen – von Unterrichtsplanung
    bis hin zu Troubleshooting-Workflows.
    """
)

st.divider()
st.subheader("Neu in Vision & Medien")
st.markdown(
    """
    - 🎨 **Image Creator** – Erzeuge Bilder direkt aus deinen Prompts.
    - 🎥 **Video Generator** – Kombiniere Szenen-Prompts zu einem Slideshow-Video mit optionalem Audiotrack.
    - 📥 **YouTube Media Studio** – Lade Videos herunter, exportiere Audio und erstelle Transkripte als Text, SRT oder VTT.
    """
)
