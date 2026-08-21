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

-- Diego Fondevilla :)

""")

tab1, tab2, tab3 = st.tabs([
    "📊 Data Visualization through Tableau and Excel", 
    "📲 Machine Learning using Python", 
    "💾 Creation and handling of SQL based databases", 
])

with tab1:

    st.markdown("""
    #### Origins of the project
    Orginally, the project involved creating different visualizations of the qualtrics data using excel. 
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

    #### Notes about design
    Once you have everything figure out, it all comes down now to how you design your sheets and dashboards. Something I found useful was using colors consistently for certain answers (Ex: Green for yes, red for no), 
    ensuring sheets have consitent metrics (Ex: Using percentage of total how your metrics in bar charts), and experementing with different charts that can properly help say my intended story. For tips on good dashboard design,
    I highly recommend checking out online examples and trying to replicate them! Once you have your final dashboards, you can host it through Tableau Public so that Kate can see your progress, and it can act as a personal portfolio.

    #### Final Notes
    While I do think that the design of the dashboards were good overall, there are definitely improvements that could be made with the filters itself. The biggest issues the filters had was that sometimes it would take too long 
    for the software to filter out data, sometimes it can take 10 seconds before a single filter works. To solve this, I wanted to make a SQL based database wherein the data would already be normalized, allowing for much better performance in filtering.
    You can find more information about this in the <u>💾 Creation and handling of SQL based databases</u> tab. 

    """, unsafe_allow_html=True)
with tab2:

    st.markdown("""
    #### How the idea of the model came to be
    After the creation of the dashboards, I was eager to implement my Machine Learning skills as a Data Scientist. I realized that while the filters I had in Tableau were useful, it was challening having to use different combinations of filters just to analyze a 
    specific group of students. That problem gave me idea of using unsupervised learning to create labels for student groups using the most prominent variables in the dataset. The variables that were used in the model are also variables that are very likely to be collected
    again in future, so creating a Machine Learning model that can also be used for future surveys became the next goal I wanted to accomplish. 

    #### Creation of the model
    First steps in creating the model was researching which model is the best one that can help solve the problem with the data I have. This lead to two possible options, a PAM model or a Hierarichal model.
    For more information of the process, check my [Github](https://github.com/diegofonde/schmid_analysis) and navigate to the models folder where you can see the ipynb file containing the code for creating the model.

    #### Putting the model into production
    Once the model creation is complete, the next step was to put it into production for future use. To be honest, the the exact steps I took to do that are hard to explain but I can give a general rundown of how I did it and what tools I used. 
    1. Downloading the metrics of the model, in this case it is the centroids of the clusters. 
    2. Creating APIs using FastAPI library that can help input data into model and retrieve results.
    3. Host your model on Render where you can use your APIs to connect to the model.
    4. Have a simple frontend like Streamlit where you can show your model works. 

    I definitely recommend you to do a lot of research on this, and take your time finding out how to implement it yourself. 

    #### Final Notes
    If you were to use this model for future projects, it is important to continually evaluate the model with new data since if there is data that a model is not familiar with, you may have to retrain the model or most likely make a new one. Ideally
    I wanted to be able to connect my model to help cluster student data that gets entered to my hosted database, but due to time and complexity I was unable to do that. Being able to create a model and put it into production is a huge skill to add 
    to your resume, so I highly recommend at least trying to learn how to do it, but for the job it isn't as necessary.
    """)
with tab3: 

    st.markdown("""
    #### Why create a Database
    Assides from the fact that databases are really useful for storing data, it is a key part of helping automate everything surrounding the project. By connecting the database to Tableau, data can be automatically be updated while also allowing for efficient filtering. 
    Connecting the hosted clustering algorithm allows for the automatic clustering of students as soon as the data related to them is entered. There are a lot of benefits of using a SQL based database if it is properly implemented.

    #### Tools and Important concepts
    To create a database, remember concepts such as Normalization while designing it in order to ensure data is stored and can be interacted with efficiently. I use a website called [dbdiagram.io](https://dbdiagram.io/home) to help visualize the design, and it makes it 
    really use to export it out for any existing database. I hosted the database on a platform called [Supabase](https://supabase.com) since it is very useful to ensuring data security.

    #### Supabase
    Supabase uses a specific type of SQL called PostgreSQL. Through it you can add different functions that can help automatically give out ids to certain tables of data, or functions that can help retrieve data a specific way. I highly recommend to learn about the different 
    features in your own time since if you were to use it or something similar, it can help make managing data a lot easier. 

    #### Final notes
    The biggest issue I had with the database is finding the best way to upload data while also storing both the raw and cleaned version of responses. Without this feature, it would be hard to be able to upload raw responses while also letting future employees clean the data in their own way.
    If this feature gets figured out, it will help in connecting the cleaned data to tableau for dashboard creation (though you would have to redesign it differently from how I originally did it), and help with letting the model cluster data. For now, I have added a feature that will let you download 
    the data in its normalized form which will let you find new ways to design the dasboard. Hopefully this feature can help with your future work!

    """)