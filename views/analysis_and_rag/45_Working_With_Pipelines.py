import os
import streamlit as st

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

st.set_page_config(page_title="RAG Pipeline MiniApp", layout="wide")
st.title("🔧 Working With Pipelines: RAG with Python & Ollama")

st.markdown("""
Upload a text or PDF document, and this app will:
- Read and summarize the content
- Answer your questions about it
- Analyse the document using a RAG pipeline (Retrieval Augmented Generation) with Ollama
""")

uploaded_file = st.file_uploader("Upload a text or PDF file", type=["txt", "pdf"])
question = st.text_input("Ask a question about the document:")

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()
    temp_file_path = f"temp_doc.{ext}"

    try:
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Loader
        if ext == "pdf":
            loader = PyPDFLoader(temp_file_path)
        else:
            loader = TextLoader(temp_file_path, encoding="utf-8")
        docs = loader.load()

        # Split
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)

        # Vector store
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectordb = FAISS.from_documents(splits, embeddings)
        retriever = vectordb.as_retriever(search_kwargs={"k": 4})

        # LLM
        llm = ChatOllama(model="llama3")

        # Summarization chain (stuff)
        summary_prompt = ChatPromptTemplate.from_template(
            "You are a concise technical summarizer.\n"
            "Summarize the following document chunks into a short overview:\n\n{context}"
        )
        summary_chain = create_stuff_documents_chain(llm=llm, prompt=summary_prompt)

        # RAG chain (retrieval + stuff)
        rag_prompt = ChatPromptTemplate.from_template(
            "Use ONLY the provided context to answer the user question.\n"
            "If the answer is not in the context, say you don't know.\n\n"
            "<context>\n{context}\n</context>\n\nQuestion: {input}"
        )
        doc_chain = create_stuff_documents_chain(llm=llm, prompt=rag_prompt)
        rag_chain = create_retrieval_chain(retriever, doc_chain)

        # ---- UI ----

        # Summary: pass a dict with the expected key for the template variable
        st.subheader("Summary")
        summary_text = summary_chain.invoke({"context": splits})
        st.write(summary_text)

        # Q&A
        if question:
            st.subheader("Answer")
            result = rag_chain.invoke({"input": question})
            st.write(result.get("answer", ""))

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
else:
    st.info("Please upload a text or PDF file to get started.")
