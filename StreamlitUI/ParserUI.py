import streamlit as st
header= st.container()
fileupload= st.container()
result=st.container()

with header:
    st.title("Welcome to my Resume Parser Project!")
    st.text("In this project we are doing parsing using nlp and scipy Library")

with fileupload:
    st.header("Upload Your Resume") 
    resume=st.file_uploader("Upload Your Resume",type=["pdf","docx","txt"])
    if st.button("Upload"):
        if resume is not None:
            st.write("File Uploaded Successfully Wait for Result")
st.markdown('##')
st.markdown('##')
# with result:
#     st.header("Result")

#     result=pd.read_csv('data1.csv')
#     st.write(result.head())