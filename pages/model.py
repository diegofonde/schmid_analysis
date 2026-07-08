import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go

st.title("📲 PAM Clustering Model")
st.markdown("""
Welcome to the student segmentation engine! This page leverages unsupervised machine learning 
to partition our student dataset into distinct, behavioral profiles based on their commuting status,
working status, number of credits enrolled, and labs enrolled.
""")

with st.expander("🧠 Deep Dive: How does the PAM Clustering Model work?"):
    st.markdown("""
    ### Partitioning Around Medoids (PAM) with Gower Distance
    Our student dataset contains a **mixed data structure** featuring ordinal variables (e.g., credits, labs) alongside numerical metrics (e.g., commuting status, working staus). Because standard distance metrics (like Euclidean distance) cannot mathematically process mixed data types well, our model employs a two-stage pipeline: 
    
    #### 1. Gower Distance Matrix Transformation
    Before clustering, the data passes through a **Gower Distance** algorithm. Gower calculates a feature-specific dissimilarity score between 0 and 1 for every pair of students:
    * **For Categorical Data:** It applies binary matching (0 if they share the same status, 1 if they do not).
    * **For Ordinal/Numerical Data:** It calculates the absolute difference divided by the total range of that feature.
    
    The result is a comprehensive similarity matrix that standardizes every student's unique combination of lifestyle factors.
    
    #### 2. Partitioning Around Medoids (PAM)
    Once the Gower matrix is built, the **PAM algorithm** selects **actual, real student profiles** from our dataset to act as the centerpoints (**medoids**) for each cluster, rather than calculating artificial 'centroids' (mathematical averages) like traditional K-Means. 
    
    **Why this pipeline matters for our analysis:**
    * **Robust Mixed-Data Handling:** Utilizing Gower distance ensures that categorical grouping labels hold appropriate mathematical weight alongside numerical features.
    * **High Robustness to Noise:** PAM uses actual medoids, making it significantly less sensitive to outliers or anomalous student schedules than K-Means.
    * **True Interpretability:** Every cluster profile is anchored to a real-world scheduling pattern, ensuring our student personas represent genuine behaviors rather than abstract mathematical fractions.
    
    #### 3. ### Model Selection & Performance
    To determine the optimal segmentation framework, the **PAM (Partitioning Around Medoids)** model's performance was benchmarked against an **Agglomerative Hierarchical Clustering** algorithm. 

    While both models achieved an identical, robust **Silhouette Score of 0.65 at k = 4**, the PAM model was selected for production based on two critical advantages:

    * **Superior Interpretability & Exemplar Profiles:** Because PAM anchors its clusters around a *medoid* (a real student profile existing within the dataset) rather than an abstract mathematical average, the resulting segments are highly interpretable. Stakeholders can look at a tangible, real-world example to immediately understand the behavioral boundaries of the entire cluster.
    * **Computational Efficiency:** The PAM algorithm demonstrates significantly faster execution times and lower memory overhead during training compared to the $O(N^2)$ time complexity of Hierarchical Clustering. This ensures the pipeline remains scalable as more student data is collected.
    
    """)

st.subheader("🎯 Student Persona Breakdown")
st.write("The PAM mode has 4 designated clusters: **On-Campus Hustlers**, **Commuting Overdrivers**, **Commuting Academics** and **On-Campus Residents**. Click through the tabs below to understand the behavioral traits defining each cluster: ")

tab1, tab2, tab3, tab4 = st.tabs([
    "🏃‍♂️ On-Campus Hustlers", 
    "🚗 Commuting Overdrivers", 
    "📚 Commuting Academics", 
    "🏠 On-Campus Residents"
])

with tab1:
    st.markdown("""
    **Core Characteristics:**
    * **Housing:** Live close to or on campus, 0- 15mins commute.
    * **Academic Load:** High unit count, takes 16-18 credits.
    * **Employment:** Is employed with work hours ranging from 1-40 hours.
    """)

with tab2:
    st.markdown("""
    **Core Characteristics:**
    * **Housing:** Off-campus commuters traveling distances ranging from over 15 minutes to an hour.
    * **Academic Load:** High unit count, takes 16-18 credits.
    * **Employment:** Is employed with work hours ranging from 1-40 hours.
    """)

with tab3:
    st.markdown("""
    **Core Characteristics:**
    * **Housing:** Off-campus commuters traveling distances ranging from over 15 minutes to an hour
    * **Academic Load:** Taking low to medium using count, takes 12-15 credits.
    * **Employment:** Is not exmployed.
    """)

with tab4:
    st.markdown("""
    **Core Characteristics:**
    * **Housing:** Live close to or on campus, 0- 15mins commute.
    * **Academic Load:** Taking low to medium using count, takes 12-15 credits.
    * **Employment:** Is not exmployed.
    """)

API_URL_PREDICT =  "https://schmid-student-segmentation-api.onrender.com/predict" # API URL for API prediction hosted in Render
API_URL_MEDOIDS =  "https://schmid-student-segmentation-api.onrender.com/medoids" # API URL for API medoids hosted in Render

st.subheader("📂 Upload your dataset here: ")
uploaded_file = st.file_uploader("Upload a CSV file", type = ["csv"])

if uploaded_file is not None:

    raw_data = pd.read_csv(uploaded_file)

    st.write("Data Preview: ")
    st.dataframe(raw_data.head())

    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = None

    if st.button("Clean Data"):

        cleaned_data = raw_data.copy()

        commuting_question = "How many minutes is your typical commute (one way)? *this includes walking, biking, driving, or public transit time"
        working_question = "How many hours per week do you typically work?"
        credits_question = "How many credits are you enrolled in this semester?"
        labs_question = "How many lab courses are you enrolled in this semester?"


        if commuting_question in cleaned_data.columns:

            conditions = [(cleaned_data[commuting_question] == '0-15 mins')]
            choices = ['non-commuter']
            cleaned_data['commuting_group'] = np.select(conditions, choices, default = 'commuter')

        if working_question in cleaned_data.columns:

            conditions = [(cleaned_data[working_question] == '0')]
            choices = ['not working']
            cleaned_data['work_group'] = np.select(conditions, choices, default = 'working')

        if credits_question in cleaned_data.columns:

            cleaned_data['credits_bin'] = pd.cut(
                cleaned_data[credits_question],
                bins = [0, 11.9, 15.1, 18.1, 100],
                labels = ['1-11', '12-15', '16-18', '18+']
            )
            cleaned_data['credits_bin'] = cleaned_data['credits_bin'].astype(str)

        cleaned_data['labs'] = cleaned_data[labs_question].astype(str)

        st.session_state.cleaned_df = cleaned_data
        st.success("Data has been cleaned")

    if st.session_state.cleaned_df is not None:
            st.write("Cleaned data Preview: ")
            st.dataframe(st.session_state.cleaned_df.head())

            if st.button("Run clustering algorithm"):

                df_clustering = st.session_state.cleaned_df.copy()

                student_list = df_clustering.to_dict(orient = "records") # Converts dataframe to a dictionary 
                payload = {"students": student_list} # List that contains dictionary of student information to match API


                with st.spinner("Calculating..."):

                    try:
                        response = requests.post(API_URL_PREDICT, json = payload)

                        if response.status_code == 200:

                            predictions = response.json()["Predictions"]

                            # Putting API response back into the dataset
                            group = []
                            group_name = []
                            for p in predictions: 
                                group.append(p['group'])
                                group_name.append(p['group_name'])

                            df_clustering["Predicted_Group"] = group
                            df_clustering["Predicted_Group_Name"] = group_name 

                            st.session_state["df_clustered_results"] = df_clustering

                        else:
                            st.error(f"The API returned an error code: {response.status_code}")
                            st.caption(f"Error Details: {response.text}") 

                    except requests.exceptions.ConnectionError:

                        st.error("Could not establish connection to the server")
                        st.error("If the server has been inactive for awhile, render may need to take 60 seconds to reactivate.")
                
            if "df_clustered_results" in st.session_state:

                    st.write("----")
                    st.subheader("🔍 Individual Student Cluster Breakdown")
                    st.markdown("Select a student and a metric to visualize exactly why they were assigned to their specific cluster.")

                    df_final = st.session_state["df_clustered_results"]

                    # Allow user to visualize every 50 clustered student
                    batch_size = 30
                    total_students = len(df_final)

                    page_options = []
                    for i in range(0, total_students, batch_size):
                        end_range = min(i + batch_size, total_students)
                        page_options.append(end_range)

                    selected_batch = st.selectbox("Selecting batch to be displayed: ", page_options)

                    current_page_idx = page_options.index(selected_batch)
                    start_idx = current_page_idx * batch_size
                    end_idx = min(start_idx + batch_size, total_students)

                    df_batch = df_final[start_idx: end_idx]

                    feature_variables = ['commuting_group', 'work_group', 'credits_bin', 'labs', 'student_id']

                    cluster_colors = ["#DC2626", "#2563EB", "#10B981", "#F59E0B"]

                    fig = px.parallel_categories (
                        df_batch,
                        dimensions = feature_variables,
                        color = "Predicted_Group",
                        color_continuous_scale = cluster_colors,
                        title = "Students by Cluster",
                        labels = {
                            "commuting_group": "Commute Status",
                            "work_group": "Working Status",
                            "credits_bin": "Credits Taken",
                            "labs": "Labs taken",
                            "student_data": "ID"
                        }
                    )

                    fig.update_layout(
                        height = 650,
                        margin = dict(l = 140, r = 140, t = 100, b = 80),
                        coloraxis_colorbar = dict (
                            title = "Group Name",
                            tickvals = [0, 1, 2, 3], # Corresponding number per group name
                            ticktext = ["On-Campus Hustlers", "Commuting Overdrivers", "Commuting Academics", "On-Campus Residents"],
                            lenmode = "pixels",
                            len = 250
                        )
                    )

                    st.plotly_chart(fig, use_container_width = True)

                    csv_output = df_final.to_csv(index = False).encode('utf-8')
                    st.download_button(
                        label = "📥 Download Segmented Dataset CSV",
                        data = csv_output,
                        file_name = "schmid_segmented_students.csv",
                        mime = "text/csv",
                        key = "download_bottom" # Unique key prevents Streamlit errors
                    )
    

