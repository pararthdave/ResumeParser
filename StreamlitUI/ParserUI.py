import streamlit as st  
from resumeparser_extractionfunctions import ResumeParser
from parsepdf import PdfParse
import pdftotext
parser=ResumeParser()   

st.sidebar.title("Resume Parser")
resume=st.sidebar.file_uploader("Upload Your Resume",type=["pdf"])
if st.sidebar.button("Upload"):
    if resume is not None:
        # f=psr(resume)
        with open(resume, "rb") as f:
            pdf = pdftotext.PDF(f)
        finalpg=[]
        for page in pdf:
            pg=page.strip()
            finalpg.append(pg)
        st.success("File Uploaded Successfully Wait for Result")
        st.text("NAME: ",parser.extract_name(finalpg))
        st.text("EMAIL: ")
        st.text("CONTACT: ")
        st.text("EMAIL: ")
        st.text("EDUCATION: ")
        st.text("EXPERIENCE: ")
        st.text("HOBBIES: ")
        st.text("SKILLS: ")
        st.text("LOCATION: ")
        st.text("EMAIL: ")
    else:
        st.error("Please select a PDF file!")
st.sidebar.text("Made with ❤️ by Team 3, Searce Inc.")
