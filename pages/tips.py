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
    **Origins of the project:** Orginally, the project involved creating different visualizations of the qualtrics data using excel. 
    While excel did help and giving a simple understanding of the data, I felt that with the amount of questions the survey contained, 
    there were ways to ways that the data can be analyzed. (Ex: Analyzing by progra or by student year)

    With this realization, I decided that Tableau was the best tool for the job due to its features of **dashboard building** and use of **dynamic filters**.

    When making the dashboards there are 2 essential steps in preparing them:
    1. Data Cleaning 
    2. Dashboard Grouping

    #### 1) Data Cleaning
    Data cleaning is important since not only do you need to ensure that the raw data can be transformed to actionable insights, but you would also need 
    to prepare the data in a way where in users can have multiple answers for the same question that can still be filtered dynamically.

    For the step by step process of how I did this, you can view it through this [Link](https://docs.google.com/document/d/1wynZxW1BWdYdv1EKf-MilKp-ROpnr6NEnZRDe1LdHUE/edit?usp=sharing).

    #### 2) Dashboard Grouping
    Once you have the data cleaned the next best thing to start planning for is figuring out which data or groups of questions should be grouped together as invididual dashboards. A good 
    starting point to figuring it out is checking out the qualtrics survey itself since often times those questions are already grouped together in their respective blocks. 

    Once you have everything figure out 

    """)
with tab2:

    st.markdown("""""")
with tab3: 

    st.markdown("""""")