import re
import json
from datetime import datetime
from textwrap import dedent
from collections import defaultdict

import streamlit as st
from lib.helper_streamlit import add_select_model, generate

# -----------------------------------------------------------------------------
st.set_page_config(page_title="Education Tutor", page_icon="📚", layout="wide")

st.title("📚 Unterrichts-Coach mit Ollama")

with st.sidebar:
    model = add_select_model()
    st.markdown(
        """
        Plane Unterrichtseinheiten mit lokalem Ollama.
        Fülle die Felder aus und erzeuge einen strukturierten Lernplan (inkl. JSON).
        """
    )

# -----------------------------------------------------------------------------
# Eingabeformular
# -----------------------------------------------------------------------------
with st.form("lesson_plan"):
    col1, col2 = st.columns(2)
    with col1:
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
        duration = st.slider("Gesamtdauer (Minuten)", 30, 240, 90, step=15)
        num_units = st.number_input(
            "Anzahl Lerneinheiten", min_value=1, max_value=12, value=3, step=1
        )
        language = st.selectbox("Ausgabesprache", ["Deutsch", "Englisch"], index=0)

    with col2:
        goals = st.text_area(
            "Lernziele (Stichpunkte)", "Lineare Funktionen verstehen und anwenden."
        )
        prerequisites = st.text_area(
            "Vorkenntnisse / Lernvoraussetzungen",
            "Grundrechenarten, Variablenverständnis",
        )
        constraints = st.text_area(
            "Einschränkungen/Settings", "Kein Internet, Whiteboard/Marker verfügbar"
        )
        tone = st.selectbox(
            "Ton & Stil",
            ["Motivierend", "Strukturiert", "Kreativ", "Experimentell"],
            index=1,
        )

    col3, col4 = st.columns(2)
    with col3:
        activities = st.text_area(
            "Bevorzugte Aktivitäten & Materialien",
            "Kurze Wiederholung, Gruppenarbeit, Mini-Quiz am Ende, Arbeitsblätter",
        )
        diff_levels = st.multiselect(
            "Leistungsniveaus berücksichtigen",
            ["Förderbedarf", "Regelniveau", "Erweitert"],
            default=["Regelniveau", "Erweitert"],
        )
    with col4:
        include_quiz = st.checkbox("Mini-Quiz einbauen", value=True)
        include_rubric = st.checkbox("Bewertungskriterien/Rubric ausgeben", value=True)
        include_homework = st.checkbox("Hausaufgaben/Weiterarbeit ausgeben", value=True)
        include_tips = st.checkbox(
            "Typische Fehlvorstellungen & Checkpoints", value=True
        )

    submitted = st.form_submit_button("🧠 Lernplan generieren")

# -----------------------------------------------------------------------------
# Prompt-Template (mit escaped Platzhaltern)
# -----------------------------------------------------------------------------
PROMPT_TEMPLATE = """\
Du agierst als **professioneller Unterrichtscoach** und Lehrplan-Designer.
Erzeuge auf Basis der Vorgaben **zwei Ausgaben**:

1) Einen **vollständig formatierten Unterrichts-/Lernplan als Markdown**.
2) Ein **valides JSON** gemäß untenstehendem Schema, eingeschlossen in einem Codeblock mit ```json Fence.

### Vorgaben
- Fach: {subject}
- Lernniveau: {level}
- Gesamtdauer: {duration} Minuten
- Anzahl der Lerneinheiten: {num_units}
- Lernziele (Stichpunkte): {goals}
- Vorkenntnisse/Voraussetzungen: {prerequisites}
- Bevorzugte Aktivitäten/Materialien: {activities}
- Einschränkungen/Settings: {constraints}
- Ton & Stil: {tone}
- Ausgabesprache: {language}
- Leistungsniveaus berücksichtigen: {diff_levels}
- Optionales Mini-Quiz: {include_quiz}
- Rubric/Bewertungskriterien: {include_rubric}
- Hausaufgaben/Weiterarbeit: {include_homework}
- Fehlvorstellungen & Checkpoints: {include_tips}

### Inhaltliche Leitplanken
- Nutze **realistische Zeitboxen**, die die Gesamtdauer nicht überschreiten.
- Verwende **präzise Lernziele** (Bloom-Taxonomie).
- **Differenzierung** für die angegebenen Leistungsniveaus.
- **Assessment**: Formativ und ggf. summativ.
- **Übungen/Aufgaben**: Mindestens fünf, mit Lösungen.
- **Fehlvorstellungen**: Liste mit Gegenstrategien.
- **Ressourcen**: Offline-tauglich bei "Kein Internet".

### Markdown-Ausgabe – Struktur
# Titel des Unterrichts
## Überblick
- Fach, Niveau, Gesamtdauer, Datumsvorschlag
- Lernziele (Liste)
- Vorkenntnisse
- Materialien
- Ablauf in Kurzform

## Inhaltsverzeichnis
- Liste aller Lerneinheiten (mit Nummer, Titel, Zeit)

## Lerneinheiten
### Einheit {{i}}: {{Titel}}
**Zeit:** {{Minuten}}  
**Ziele:** …  
**Inhalt & Erklärungen:** …  
**Vorgehen (Schritt-für-Schritt):** …  
**Differenzierung:** …  
**Checkpoints/Formatives Assessment:** …  
**Materialien:** …

(repliziere für alle Einheiten)

## Aktivitäten & Übungen
- Mindestens 5 Aufgaben (Leicht/Mittel/Schwer), **jeweils mit Lösung**.
{optional_quiz}

## Reflexion
- Lehrer*in-Reflexion und Lernenden-Reflexion (2–3 Leitfragen)

## Hausaufgabe/Weiterarbeit
- Aufgaben mit Zeitangaben und **Lösungen**

## Bewertungskriterien (Rubric)
- Kriterienraster (4 Stufen) mit kurzen Deskriptoren

## Typische Fehlvorstellungen & Gegenstrategien
- Liste (Fehlannahme → Gegenstrategie)
- Diagnosefragen

### JSON-Ausgabe – Schema (in ```json Fence ausgeben)
Das JSON MUSS valide sein und **NUR** dieses Schema enthalten:

{{
  "title": "string",
  "subject": "string",
  "level": "string",
  "total_duration_min": {duration},
  "units": [
    {{
      "index": 1,
      "title": "string",
      "duration_min": 0,
      "objectives": ["..."],
      "steps": ["..."],
      "materials": ["..."],
      "differentiation": {{
        "Foerderbedarf": ["..."],
        "Regelniveau": ["..."],
        "Erweitert": ["..."]
      }},
      "checkpoints": ["..."]
    }}
  ],
  "exercises": [
    {{
      "difficulty": "Leicht|Mittel|Schwer",
      "prompt": "string",
      "solution": "string"
    }}
  ],
  "quiz": [{{
    "question": "string",
    "choices": ["A", "B", "C", "D"],
    "answer": "A"
  }}],
  "rubric": [{{
    "criterion": "string",
    "levels": [{{
      "name": "string",
      "descriptor": "string"
    }}]
  }}],
  "homework": [{{
    "task": "string",
    "solution": "string"
  }}],
  "misconceptions": [{{
    "misconception": "string",
    "fix": "string"
  }}]
}}

WICHTIG:
- Liefere zuerst die **Markdown-Sektion**, danach **genau einen** ```json Codeblock.
- Keine zusätzlichen Codeblöcke außer diesem.
"""

# -----------------------------------------------------------------------------
# JSON-Extraktion
# -----------------------------------------------------------------------------
JSON_FENCE_RE = re.compile(r"```json\s*(\{.*\})\s*```", re.DOTALL)


def extract_json_block(text: str):
    match = JSON_FENCE_RE.search(text or "")
    if not match:
        return None, "Kein JSON-Block gefunden."
    raw = match.group(1)
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as e:
        return None, f"JSON fehlerhaft: {e}"


# -----------------------------------------------------------------------------
# Submit: Generiere Lernplan
# -----------------------------------------------------------------------------
if submitted:
    safe_vars = defaultdict(
        str,
        {
            "subject": subject,
            "level": level,
            "duration": duration,
            "num_units": num_units,
            "goals": goals,
            "prerequisites": prerequisites,
            "activities": activities,
            "constraints": constraints,
            "tone": tone,
            "language": language,
            "diff_levels": ", ".join(diff_levels) if diff_levels else "Regelniveau",
            "include_quiz": "Ja" if include_quiz else "Nein",
            "include_rubric": "Ja" if include_rubric else "Nein",
            "include_homework": "Ja" if include_homework else "Nein",
            "include_tips": "Ja" if include_tips else "Nein",
            "optional_quiz": "- Füge ein kurzes, auswertbares Mini-Quiz mit Lösungen hinzu."
            if include_quiz
            else "",
        },
    )

    prompt = dedent(PROMPT_TEMPLATE).format_map(safe_vars)

    # LLM-Aufruf
    with st.spinner():
        llm_text = generate(model, prompt)

    # Tabs zur Anzeige
    tab_plan, tab_json, tab_raw = st.tabs(["📄 Plan", "🧩 JSON", "🗒️ Rohtext"])

    with tab_plan:
        st.markdown(llm_text)

    with tab_json:
        data, err = extract_json_block(llm_text)
        if err:
            st.warning(err)
        else:
            import pandas as pd

            st.subheader(data.get("title", "Lernplan"))
            st.caption(
                f"{data.get('subject', '')} • {data.get('level', '')} • {data.get('total_duration_min', 0)} Minuten"
            )

            if data.get("units"):
                units_df = pd.DataFrame(
                    [
                        {
                            "Einheit": u.get("index"),
                            "Titel": u.get("title"),
                            "Dauer (min)": u.get("duration_min"),
                            "Ziele": " • ".join(u.get("objectives", [])),
                            "Checkpoints": " • ".join(u.get("checkpoints", [])),
                        }
                        for u in data["units"]
                    ]
                )
                st.dataframe(units_df, width='stretch')

                with st.expander("Einheiten – Details"):
                    for u in data["units"]:
                        st.markdown(
                            f"**{u.get('index')}. {u.get('title')}** – {u.get('duration_min')} min"
                        )
                        st.markdown(f"- Ziele: {', '.join(u.get('objectives', []))}")
                        st.markdown(f"- Schritte: {' | '.join(u.get('steps', []))}")
                        st.markdown(
                            f"- Materialien: {', '.join(u.get('materials', []))}"
                        )
                        diff = u.get("differentiation", {})
                        if diff:
                            st.markdown("- Differenzierung:")
                            for k, v in diff.items():
                                st.markdown(f"  - {k}: {', '.join(v)}")
                        st.markdown(
                            f"- Checkpoints: {', '.join(u.get('checkpoints', []))}"
                        )
                        st.markdown("---")

            if data.get("exercises"):
                st.subheader("Übungen")
                for i, ex in enumerate(data["exercises"], 1):
                    st.markdown(
                        f"**Aufgabe {i} ({ex.get('difficulty', '?')})**: {ex.get('prompt', '')}"
                    )
                    st.markdown(
                        f"<details><summary>Lösung</summary><p>{ex.get('solution', '')}</p></details>",
                        unsafe_allow_html=True,
                    )

            if data.get("quiz"):
                st.subheader("Mini-Quiz")
                for i, q in enumerate(data["quiz"], 1):
                    st.markdown(f"**Frage {i}:** {q.get('question', '')}")
                    st.markdown("Optionen: " + ", ".join(q.get("choices", [])))
                    st.caption(f"Antwort: **{q.get('answer', '')}**")

            if data.get("rubric"):
                st.subheader("Bewertungskriterien (Rubric)")
                for r in data["rubric"]:
                    st.markdown(f"- **{r.get('criterion', '')}**")
                    for lvl in r.get("levels", []):
                        st.markdown(
                            f"  - {lvl.get('name', '')}: {lvl.get('descriptor', '')}"
                        )

            if data.get("homework"):
                st.subheader("Hausaufgabe/Weiterarbeit")
                for h in data["homework"]:
                    st.markdown(f"- **Aufgabe:** {h.get('task', '')}")
                    if h.get("solution"):
                        st.markdown(f"  - Lösung: {h.get('solution', '')}")

            if data.get("misconceptions"):
                st.subheader("Typische Fehlvorstellungen & Gegenstrategien")
                for m in data["misconceptions"]:
                    st.markdown(f"- **Fehlannahme:** {m.get('misconception', '')}")
                    st.markdown(f"  - **Gegenstrategie:** {m.get('fix', '')}")

            # Downloads
            md_bytes = llm_text.encode("utf-8")
            st.download_button(
                "⬇️ Plan als Markdown",
                data=md_bytes,
                file_name=f"lernplan_{subject}_{datetime.now().date()}.md",
                mime="text/markdown",
            )

            json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button(
                "⬇️ Struktur als JSON",
                data=json_bytes,
                file_name=f"lernplan_{subject}_{datetime.now().date()}.json",
                mime="application/json",
            )

    with tab_raw:
        st.code(llm_text or "", language="markdown")
