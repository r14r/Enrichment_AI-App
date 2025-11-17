import streamlit as st
from lib.helper_streamlit import add_select_model, generate

st.set_page_config(page_title="Chat Sandbox", page_icon="💬")

st.title("💬 Chat")
model = add_select_model()

st.session_state.setdefault("hist", [])

user = st.text_input("Nachricht", "")
if st.button("Senden") and user.strip():
    st.session_state["hist"].append({"role": "user", "content": user})
    prompt = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state["hist"])

    with st.spinner():
        reply = generate(model, prompt)
        st.session_state["hist"].append({"role": "assistant", "content": reply})

for m in st.session_state["hist"][-8:]:
    st.markdown(f"**{m['role'].upper()}**: {m['content']}")
