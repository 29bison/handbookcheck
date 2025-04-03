
import streamlit as st
import fitz  # PyMuPDF
import openai
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]  # ✅ secure from Streamlit Cloud

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Ask GPT a question based on the document
def answer_question(text, question):
    prompt = f"Based on the following document, answer this question:\n\n{text}\n\nQuestion: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Streamlit UI
st.title("PDF Q&A App")

pdf_file = st.file_uploader("Upload a PDF", type="pdf")
json_file = st.file_uploader("Upload your questions (.json)", type="json")

if pdf_file and json_file:
    st.success("Files uploaded successfully!")

    with st.spinner("Reading PDF..."):
        document_text = extract_text_from_pdf(pdf_file)

    questions = json.load(json_file)

    st.subheader("Answers:")
    for q in questions:
        answer = answer_question(document_text, q)
        st.markdown(f"**Q: {q}**\n\nA: {answer}\n")
