import streamlit as st

st.set_page_config(page_title="Enrichment MiniApps", page_icon="⚡", layout="wide")

chat_and_content = [
    st.Page("views/chat_and_content/11_Chat_Sand_Box.py", title="💬 Chat Sand Box"),
    st.Page("views/chat_and_content/12_Chat_Advanced.py", title="🧠 Chat Advanced"),
    st.Page("views/chat_and_content/21_Blog_Generator_Lite.py", title="📝 Blog Generator Lite"),
    st.Page("views/chat_and_content/22_Blog_Writer.py", title="📝 Blog Writer"),
    st.Page("views/chat_and_content/26_Translator_Style.py", title="🌐 Translator Style"),
    st.Page("views/chat_and_content/27_Meeting_Notes_Condenser.py", title="📝 Meeting Notes Condenser"),
    st.Page("views/chat_and_content/28_Paraphraser_Shortener.py", title="✂️ Paraphraser & Shortener"),
    st.Page("views/chat_and_content/52_FAQ_Generator.py", title="❓ FAQ Generator"),
    st.Page("views/chat_and_content/55_Ideas_Generator.py", title="💡 Ideas Generator"),
    
]

vision_and_media = [
    st.Page("views/vision_and_media/31_Image_Analyzer.py", title="🖼️ Image Analyzer"),
    st.Page("views/vision_and_media/32_Vision_Captioner.py", title="🎬 Vision Captioner"),
    st.Page("views/vision_and_media/33_Vision_Moderation_Light.py", title="👮 Vision Moderation Light"),
    st.Page("views/vision_and_media/34_Image_Creator.py", title="🎨 Image Creator"),
    st.Page("views/vision_and_media/38_TikTok_Content_Studio.py", title="🎞️ TikTok Content Studio"),
    st.Page("views/vision_and_media/41_Local_Video_Generator.py", title="🏠 Local Video Generator"),
    st.Page("views/vision_and_media/42_Local_Image_Generator.py", title="🎨 Local Image Generator"),
]

analysis_and_rag = [
    st.Page("views/analysis_and_rag/41_Document_Analyzer.py", title="📋 Document Analyzer"),
    st.Page("views/analysis_and_rag/42_CSV_Q_And_A.py", title="📊 CSV Q&A"),
    st.Page("views/analysis_and_rag/43_PDF_Q_And_A.py", title="📄 PDF Q&A")
]


new_use_cases = [
    st.Page("views/new_use_cases/58_Education_Tutor.py", title="📚 Education Tutor"),
    st.Page("views/new_use_cases/62_Healthcare_Case_Notes.py", title="🏥 Healthcare Case Notes"),
    st.Page("views/new_use_cases/63_HR_Interview_Designer.py", title="🧑‍💼 HR Interview Designer"),
    st.Page("views/new_use_cases/64_Travel_Itinerary_Crafter.py", title="✈️ Travel Itinerary Crafter"),

]

navigation = st.navigation(
    {
        "🏠 Start": [st.Page("views/Start.py", title="🏠 Übersicht")],
        "💬 Sprache & Inhalte": chat_and_content,
        "🖼️ Vision & Medien": vision_and_media,
        "📊 Analyse & RAG": analysis_and_rag,
        "🚀 Neue Use Cases": new_use_cases,
    }
)
navigation.run()
