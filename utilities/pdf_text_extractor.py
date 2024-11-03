import streamlit as st
import PyPDF2

st.title("PDF Text Extractor")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

if pdf_file is not None:
    text = extract_text_from_pdf(pdf_file)
    st.write("PDF text extracted successfully.")
