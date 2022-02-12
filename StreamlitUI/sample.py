import pdfminer
from pdfminer.high_level import extract_pages
import streamlit as st

st.write(pdfminer.__version__)  

uploaded_file = st.file_uploader("Choose a file", "pdf")
if uploaded_file is not None:
    for page_layout in extract_pages(uploaded_file):
        for element in page_layout:
            st.write(element)