import streamlit as st  
st.sidebar.title("Resume Parser")
resume=st.sidebar.file_uploader("Upload Your Resume",type=["pdf"])
if st.sidebar.button("Upload"):
    if resume is not None:
        st.success("File Uploaded Successfully Wait for Result")
    else:
        st.error("Please select a pdf file!")
st.markdown('##')
st.markdown('##')
st.sidebar.text("Made with ❤️ by Team 3, Searce Inc.")
