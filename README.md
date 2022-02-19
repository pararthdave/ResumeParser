# ResumeParser
![Logo](/dataset/SearceLogo.png "Logo")
### Purpose


The purpose of this project is to build an able resume parser to extract important entities such as names, contact info, email, skills etc. 

It’s often a very hectic task for HR employees in order to extract all these entities manually from a varying range of resume styles. We attempt to create a resume parser that can handle varying formats of unstructured resumes and tries to extract meaningful information. 




### Approach


We tried many different libraries and approaches in order to optimize our project. We majorly used pdftotext for pdf to raw text, regex to identify and accomplish pattern based matching and Spacy/NLTK to detect entities such as names ( set of two or more consecutive proper nouns), skills etc. In order to create the front-end for this system, we have used Streamlit.





### Challenges


The major challenges that were faced during this project included:
Inaccuracy in experience and skill extraction
Detecting roll numbers as contact numbers at times
Not able to detect education year properly
Proper output for the hobbies/ achievement section is missing due to lack of proper dataset for matching.



### Future Scope


We’re planning to improve this system further by implementing a reinforcement learning based model and improve by optimizing our approaches further. We also plan to deploy this system as a webapp that can be accessed by anyone on a public server. 




### Screenshot


![ss](/ss.png "ss")

