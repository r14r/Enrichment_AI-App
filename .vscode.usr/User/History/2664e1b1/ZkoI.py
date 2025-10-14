import streamlit as st
from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="Education Tutor", page_icon="📚")

st.title("📚 Unterrichts-Coach mit Ollama")

with st.sidebar:
    model = add_select_model()
    st.markdown(
        """
        Verwende Ollama, um Unterrichtseinheiten zu planen. 
        Passe Fach, Lernziele und gewünschte Aktivitäten an.
        """
    )

with st.form("lesson_plan"):
    subject = st.text_input("Fach", "Mathematik")
    level = st.selectbox(
        "Lernniveau",
        [
            "Grundschule",
            "Unterstufe",
            "Mittelstufe",
            "Oberstufe",
            "Universität",
            "Berufliche Weiterbildung",
        ],
        index=2,
    )
    goals = st.text_area(
        "Lernziele",
        "Lineare Funktionen verstehen und anwenden.",
    )
    activities = st.text_area(
        "Aktivitäten & Materialien",
        "Kurze Wiederholung, Gruppenarbeit, Mini-Quiz am Ende.",
    )
    duration = st.slider("Dauer der Einheit (Minuten)", 30, 180, 60, step=15)
    tone = st.selectbox(
        "Ton & Stil",
        [
            "Motivierend",
            "Strukturiert",
            "Kreativ",
            "Experimentell",
        ],
        index=0,
    )
    submitted = st.form_submit_button("🧠 Lernplan generieren")

if submitted:
    prompt = f"""Du bist ein professioneller Unterrichtscoach. Erstelle einen detaillierten Unterrichtsplan.
Fach: {subject}
Lernniveau: {level}
Dauer: {duration} Minuten
Ziele: {goals}
Vorgesehene Aktivitäten oder Materialien: {activities}
Ton & Stil: {tone}

Gib eine strukturierte Antwort mit folgenden Abschnitten: 
- Einstieg

- Hauptteil
  Beschreibe den Hauptteil. Erstelle ein Inhaltserzeichnis aller Themen und Einheiten.
  Beschreibe jene Einheit mit einer Zusammenfassung
  
- Aktivität/Übung
- Reflexion

- Hausaufgabe/Weiterarbeit
  Erstelle mindests 5 Augaben. Füge am Ende die Lösungen für jede Aufgabe hinzu

Ergänze konkrete Zeitvorschläge.
"""
    with st.spinner():
        generate(model, prompt)
