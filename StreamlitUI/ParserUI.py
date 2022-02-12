import streamlit as st  
from resumeparser_extractionfunctions import ResumeParser
from parsepdf import PdfParse
import pdftotext
import nltk
from pdfminer.high_level import extract_pages
parser=ResumeParser()   


st.sidebar.title("Resume Parser")
resume=st.sidebar.file_uploader("Upload Your Resume",type=["pdf"])
# print(dir(resume))
if st.sidebar.button("Upload"):
    if resume is not None:
        # with open(resume.getvalue(), "rb") as f:
        pdf = pdftotext.PDF(resume)
        finalpg=''
        for page in pdf:
            pg=page.strip()
            finalpg+=pg
        st.success("File Uploaded Successfully Wait for Result")
        st.write("NAME: ",parser.extract_name(finalpg))
        st.write("CONTACT: ", parser.extract_phone_number(finalpg))
        st.write("EMAIL: ", str(parser.extract_email(finalpg)))
        st.write("SOCIAL MEDIA: ", parser.extract_socialmedia(finalpg))
        st.write("EDUCATION: ")
        st.write("EXPERIENCE: ")
        st.write("HOBBIES: ")
        st.write("SKILLS: ", parser.extract_skills(finalpg))
        st.write("LOCATION: ", parser.extract_location(finalpg))
    else:
        st.error("Please select a PDF file!")
st.sidebar.text("Made with ❤️ by Team 3, Searce Inc.")
