import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title("PAM Clustering Model")
st.markdown("Here is the page dedicated to clustering students based on the inputted dataset!")

API_URL =  "https://schmid-student-segmentation-api.onrender.com" # API URL for API being hosted in Render

st.subheader("📂 Upload your dataset here: ")
uploaded_file = st.file_uploader("Upload a CSV file", type = ["csv"])

if uploaded_file is not None:

    raw_data = pd.read_csv(uploaded_file)

    st.write("Data Preview: ")
    st.dataframe(raw_data.head())

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

        cleaned_data['labs'] = cleaned_data[labs_question]

        if st.button("Run clustering algorithm"):

            student_list = cleaned_data.to_dict(orient = "records") # Converts dataframe to a dictionary 
            payload = {"students": student_list} # List that contains dictionary of student information to match API


            with st.spinner("Calculating..."):

                try:
                    response = requests.post(API_URL, json = payload)

                    if response.status_code == 200:

                        predictions = response.json()["Predictions"]

                        # Putting API response back into the dataset
                        group = []
                        group_name = []
                        for p in predictions: 
                            group.append(p['group'])
                            group_name.append(p['group_name'])

                        raw_data["Predicted_Group"] = group
                        raw_data["Predicted_Group_Name"] = group_name 

                        csv_output = raw_data.to_csv(index = False).encode('utf-8')
                        st.download_button(
                            label = "📥 Download Segmented Dataset CSV",
                            data = csv_output,
                            file_name = "schmid_segmented_students.csv",
                            mime = "text/csv"
                        )
                    else:
                        st.error(f"The API returned an error code: {response.status_code}")
                        st.caption(f"Error Details: {response.text}") 

                except requests.exceptions.ConnectionError:

                    st.error("Could not establish connection to the server")
                    st.error("If the server has been inactive for awhile, render may need to take 60 seconds to reactivate.")

