import streamlit as st
import pandas as pd
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

    if st.button("Run clustering algorithm"):

        student_list = raw_data.to_dict(orient = "records") # Converts dataframe to a dictionary 
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

