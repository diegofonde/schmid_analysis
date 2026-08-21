import streamlit as st

st.title("Tips and notes for the next employee!!!📝")

st.markdown("""
Welcome to the page dedicated for tips and notes! This page contains notes that will hopefully help future employees of this position 
replicate my previous work or find ways to improve it!

**Notes are divided in 3 ways:**
* 📊 **Data Visualization through Tableau and Excel**.
* 📲 **Machine Learning using Python**
* 💾 **Creation and handling of SQL based databases**

To the next student taking up the role, I truly hope that these notes help you not only do well in the job but also grow as a Data Scientist. 
I know that the role does have big shoes to fill, but as along as you have the eagerness to learn you'll do great!
If you ever need any help, feel free to contact me! 

- Diego Fondevilla :)

""")

tab1, tab2, tab3 = st.tabs([
    "📊 Data Visualization through Tableau and Excel", 
    "📲 Machine Learning using Python", 
    "💾 Creation and handling of SQL based databases", 
])

with tab1:

    st.markdown("""
    **Origins of the project: ** Orginally, the project involved creating different visualizations of the qualtrics data using excel. 
    While excel did help and giving a simple understanding of the data, I felt that with the amount of questions the survey contained, 
    there were ways to ways that the data can be analyzed. (Ex: Analyzing by program, by student year)

    With this realization, I decided that Tableau was the best tool for the job due to its features of **dashboard building** and use of **dynamic filters**.

    """)