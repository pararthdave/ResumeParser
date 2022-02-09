import streamlit as st  
st.sidebar.title("Resume Parser")
resume=st.sidebar.file_uploader("Upload Your Resume",type=["pdf"])
if st.sidebar.button("Upload"):
    if resume is not None:
        st.success("File Uploaded Successfully Wait for Result")
    else:
        st.error("Please select a pdf file!")
st.markdown('##')
<<<<<<< HEAD
st.markdown('##') 
# with result:
#     st.header("Result")

#     result=pd.read_csv('data1.csv')
#     st.write(result.head())
=======
st.markdown('##')
st.sidebar.text("Made with ❤️ by Team 3, Searce Inc.")
>>>>>>> 6eaa7916bb77e0dacade9992d3b2b6bc4f9264d5
