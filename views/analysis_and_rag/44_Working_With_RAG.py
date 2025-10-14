import tempfile
import os

import streamlit as st

from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredImageLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

from lib.helper_streamlit import add_select_model

st.set_page_config(page_title="RAG MiniApp", page_icon="🔍")
st.title("🔍 Minimal RAG App for PDF, TXT, and Images (Ollama Local)")

uploaded_file = st.file_uploader("Upload a PDF, TXT, or Image file", type=["pdf", "txt", "png", "jpg", "jpeg"])

if not uploaded_file:
    st.info("Upload a PDF, TXT, or image file to get started.")    
else:
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load document
        if uploaded_file.name.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif uploaded_file.name.lower().endswith(".txt"):
            loader = TextLoader(file_path)
        elif uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
            loader = UnstructuredImageLoader(file_path)
        else:
            st.error("Unsupported file type.")
            st.stop()

        docs = loader.load()
        st.success(f"Loaded {len(docs)} document chunk(s).")

        # Embeddings and Vectorstore
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.from_documents(docs, embeddings)

        # LLM (using Ollama locally)
        model = add_select_model()
        if not model:
            st.info("Please enter the Ollama model name to proceed.")
        else:            
            llm = Ollama(
                model=model,
                temperature=0.1,
                max_tokens=256,
            )
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=db.as_retriever(),
                return_source_documents=True,
            )

            query = st.text_input("Ask a question about your document:")
            if query:
                with st.spinner("Generating answer..."):
                    result = qa({"query": query})
                st.markdown("**Answer:**")
                st.write(result["result"])
                st.markdown("**Source Document(s):**")
                for i, doc in enumerate(result["source_documents"]):
                    st.write(f"Chunk {i+1}: {doc.page_content[:300]}...")
