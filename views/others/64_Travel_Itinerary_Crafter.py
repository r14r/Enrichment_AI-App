import streamlit as st
from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="Travel Itinerary Crafter", page_icon="✈️")

st.title("✈️ Reiseplan-Generator")

with st.sidebar:
    model = add_select_model()
    st.markdown(
        "Erstelle individuelle Reisepläne inklusive Highlights, Budget und Tipps."
    )

with st.form("travel_form"):
    destination = st.text_input("Reiseziel", "Lissabon")
    duration = st.slider("Reisedauer (Tage)", 2, 21, 5)
    travelers = st.text_input("Wer reist mit?", "Paar, abenteuerlustig")
    interests = st.multiselect(
        "Interessen",
        [
            "Kultur & Museen",
            "Kulinarik",
            "Outdoor & Natur",
            "Nachtleben",
            "Erholung",
            "Familienaktivitäten",
            "Sport",
        ],
        default=["Kultur & Museen", "Kulinarik"],
    )
    budget_level = st.selectbox(
        "Budgetniveau",
        ["Backpacker", "Mittelklasse", "Premium", "Luxus"],
        index=1,
    )
    must_do = st.text_area(
        "Must-do / Rahmenbedingungen",
        "Besuch eines Fado-Konzerts, mind. ein Tagesausflug ans Meer.",
    )
    submitted = st.form_submit_button("🧭 Reiseplan erstellen")

if submitted:
    prompt = f"""Du bist Reiseplaner:in. Erstelle einen Tagesplan für eine Reise.
Reiseziel: {destination}
Reisedauer: {duration} Tage
Reisende: {travelers}
Interessen: {', '.join(interests) if interests else 'offen'}
Budgetniveau: {budget_level}
Must-do: {must_do}

Gib für jeden Tag Morgen-, Nachmittag- und Abendprogramm, Restauranttipps, Budgetschätzung und praktische Hinweise.
"""
    generate(model, prompt)
