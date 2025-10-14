import streamlit as st

st.set_page_config(page_title="Enrichment MiniApps", page_icon="⚡", layout="wide")

chat_and_content = [
    st.Page("views/chat_and_content/11_Chat_Sand_Box.py", title="💬 Chat"),
    st.Page("views/chat_and_content/12_Chat_Advanced.py", title="🧠 Chat Advanced"),
    st.Page("views/chat_and_content/21_Blog_Generator_Lite.py", title="📝 Blog Generator"),
    st.Page("views/chat_and_content/52_FAQ_Generator.py", title="❓ FAQ Generator"),
    st.Page("views/chat_and_content/55_Ideas_Generator.py", title="💡 Ideas Generator"),
    
]

vision_and_media = [
    st.Page("views/vision_and_media/31_Image_Analyzer.py", title="👮 Bildanalyse"),
    st.Page("views/vision_and_media/33_Vision_Moderation_Light.py", title="👮 Bilder"),
]

analysis_and_rag = [
    st.Page("views/analysis_and_rag/42_CSV_Q_And_A.py", title="📊 CSV Q&A"),
    st.Page("views/analysis_and_rag/43_PDF_Q_And_A.py", title="📄 PDF Q&A")
]


new_use_cases = [
    st.Page("views/new_use_cases/58_Education_Tutor.py", title="📚 Unterrrichts-Coach"),
    st.Page("views/new_use_cases/64_Travel_Itinerary_Crafter.py", title="✈️ Reiseplan-Generator"),

]

navigation = st.navigation(
    {
        "🏠 Start": [st.Page("views/Start.py", title="🏠 Übersicht")],
        "💬 Chat": chat_and_content,
        "🖼️ Bilder analysieren": vision_and_media,
        "📊 Dokumente analysieren": analysis_and_rag,
        "🚀 Weitere Beispiele": new_use_cases,
    }
)
navigation.run()
