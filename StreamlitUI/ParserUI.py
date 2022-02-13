import streamlit as st  
from resumeparser_extractionfunctions import ResumeParser
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
        st.write("NAME: ",parser.extract_name(finalpg))
        st.write("CONTACT: ", parser.extract_phone_number(finalpg))
        st.write("EMAIL: ", str(parser.extract_email(finalpg)))
        st.write("LINKEDIN: ", str(parser.extract_linkedin(finalpg)))
        st.write("GITHUB: ", str(parser.extract_github(finalpg)))
        st.write("EDUCATION: ", str(parser.extract_text(finalpg)))
        st.write("EXPERIENCE: ", str(parser.extract_experience(finalpg)))
        st.write("HOBBIES: ", str(parser.extract_hobby(finalpg)))
        st.write("SKILLS: ", str(parser.extract_skills(finalpg)))
        st.write("LANGUAGES: ", str(parser.extract_language(finalpg)))
        st.write("LOCATION: ", str(parser.locationExtraction(finalpg)))
    else:
        st.error("Please select a PDF file!")
st.sidebar.text("Made with ❤️ by Team 3, Searce Inc.")
