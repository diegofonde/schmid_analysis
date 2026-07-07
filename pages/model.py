import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go

st.title("PAM Clustering Model")
st.markdown("Here is the page dedicated to clustering students based on the inputted dataset!")

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
            st.write("Data Preview: ")
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

                    df_final = st.session_state["df_clustered_results"]

                    st.write("----")
                    st.subheader("🔍 Individual Student Cluster Breakdown")
                    st.markdown("Select a student and a metric to visualize exactly why they were assigned to their specific cluster.")

                    # Dropdowns for filtering between studeets and variables
                    student_ids = df_final['student_id'].tolist()
                    student_select = st.selectbox("Select a student", options = student_ids)

                    if student_select is not None:

                        try:

                            response = requests.post(API_URL_MEDOIDS, json = payload)

                            if response.status_code == 200:

                                # Putting medoid features in dataset 
                                predictions = response.json()["Medoid_Features"]
                                medoid_df = pd.DataFrame(predictions)
                                st.dataframe(medoid_df.head())

                            else:
                                st.error(f"API Error: Received status code {response.status_code}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Connection failed: Received status code {requests.status_code}")
                        
                        student_row = df_final[df_final['student_id'] == student_select].iloc[0] # Grabs the first student row that has that corresponding id

                        # fig = px.parallel_categories

                        # category_distributions = df_final.groupby(['Predicted_Group_Name', variable_select]).size().unstack(fill_value=0)
                        # category_distributions_pct = category_distributions.div(category_distributions.sum(axis=1), axis=0).reset_index()
                        # category_distributions_melted = category_distributions_pct.melt(id_vars='Predicted_Group_Name', value_name='Percentage')

                        # fig = px.bar(
                        #     category_distributions_melted,
                        #     x = "Predicted_Group_Name",
                        #     y = "Percentage",
                        #     color = variable_select,
                        #     barmode = 'group',
                        #     title = f"Categorical Proportions of {variable_select} Across Clusters",
                        #     labels = {'Percentage': 'Proportion of Cluster Population'}
                        # )

                        # st.plotly_chart(fig, use_container_width=True)

                    csv_output = df_final.to_csv(index = False).encode('utf-8')
                    st.download_button(
                        label = "📥 Download Segmented Dataset CSV",
                        data = csv_output,
                        file_name = "schmid_segmented_students.csv",
                        mime = "text/csv",
                        key = "download_bottom" # Unique key prevents Streamlit errors
                    )
    

