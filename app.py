import streamlit as st
from extractor import extract_text_from_pdf, upload_pdf_to_blob
from vector_s import VectorStore
from qa_sys import ask_gpt

st.title("Your Helper is here! to assist in all your research work)")

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type=["pdf"])
if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    upload_pdf_to_blob(uploaded_file.name, uploaded_file.name)
    text = extract_text_from_pdf(uploaded_file.name)

    vector_store = VectorStore()
    vector_store.add_text(text)

    st.success("PDF uploaded & processed successfully!")

question = st.text_input("Ask a question about the paper:")
if question:
    relevant_text = " ".join(vector_store.search(question))
    answer = ask_gpt(question, relevant_text)
    st.subheader("AI Response:")
    st.write(answer)
