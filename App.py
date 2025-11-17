import streamlit as st

st.set_page_config(page_title="Enrichment MiniApps", page_icon="⚡", layout="wide")

streamlit_samples = [
    st.Page("views/streamlit/01_Hello.py", title="👋 Hello"),
    st.Page("views/streamlit/02_Charts.py", title="📈 Charts"),
    st.Page("views/streamlit/03_DataFrames.py", title="📋 DataFrames"),
    st.Page("views/streamlit/04_LM_Chat.py", title="🤖 LM Chat"),
    st.Page("views/streamlit/05_Computer_Vison.py", title="👁️ Computer Vision"),
    st.Page("views/streamlit/06_Geospital.py", title="🌍 Geospatial"),
    st.Page("views/streamlit/11_Animation_Demo.py", title="🏠 Animation"),
    st.Page("views/streamlit/12_Dataframe_Demo.py", title="🗺️ DataFrame"),
    st.Page("views/streamlit/13_Mapping_Demo.py", title="📹 Mapping"),
    st.Page("views/streamlit/14_Plotting_Demo.py", title="📊 Plotting"),
]

chat_and_content = [
    st.Page("views/chat_and_content/11_Chat.py", title="💬 Chat"),
    st.Page("views/chat_and_content/12_Chat_Advanced.py", title="🧠 Chat Advanced"),
    st.Page("views/chat_and_content/21_Blog_Generator.py", title="📝 Blog Generator"),
    st.Page("views/chat_and_content/52_FAQ_Generator.py", title="❓ FAQ Generator"),
    st.Page("views/chat_and_content/55_Ideas_Generator.py", title="💡 Ideas Generator"),
    
]

vision_and_media = [
    st.Page("views/vision_and_media/31_Image_Analyzer.py", title="👮 Bildanalyse"),
]

analysis_and_rag = [
    st.Page("views/analysis_and_rag/42_CSV_Q_And_A.py", title="📊 CSV"),
    st.Page("views/analysis_and_rag/43_PDF_Q_And_A.py", title="📄 PDF")
]


others = [
    st.Page("views/others/58_Education_Tutor_1.py", title="📚 Unterrrichts-Coach 1"),
    st.Page("views/others/58_Education_Tutor_2.py", title="📚 Unterrrichts-Coach 2"),
    st.Page("views/others/64_Travel_Itinerary_Crafter.py", title="✈️ Reiseplan-Generator"),

]

navigation = st.navigation(
    pages = {
        "🏠 Start": [st.Page("views/Start.py", title="Übersicht")],
        "🔷 Streamlit": streamlit_samples,
        "💬 Prompts und Content": chat_and_content,
        "🖼️ Bilder": vision_and_media,
        "📊 Q & A": analysis_and_rag,
        "🚀 Weitere Beispiele": others,
    },
    position="top"
)
navigation.run()
