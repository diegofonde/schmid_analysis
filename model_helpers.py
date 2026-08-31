import pandas as pd
import requests
import streamlit as st

API_URL_PREDICT =  "https://schmid-student-segmentation-api.onrender.com/predict" # API URL for API prediction hosted in Render
API_URL_MEDOIDS =  "https://schmid-student-segmentation-api.onrender.com/medoids" # API URL for API medoids hosted in Render

def predict(df):

    student_list = df.to_dict(orient = "records") # Converts dataframe to a dictionary 
    payload = {"students": student_list} # List that contains dictionary of student information to match API

    with st.spinner("Calculating..."):

        try:

            response = requests.post(API_URL_PREDICT, json = payload)

            if response.status_code == 200:
        

                # Putting API response back into a dataframee
                predictions = response.json().get("Predictions", [])

                new_predictions = [
                    {
                        "respondent_id": df['respondent_id'].iloc[i],
                        "cluster_id": pred['group'],
                    }
                    for i, pred in enumerate(predictions)
                ]

                return new_predictions
            
            # Explicit error handling UI
            st.error(f"The API returned an error code: {response.status_code}")
            st.caption(f"Error Details: {response.text}")
            return None
            
        except requests.exceptions.Timeout:
            st.error("Request timed out.")
            st.info("Render free-tier web services spin down after inactivity. Give it 60 seconds to wake up and try again.")
            return None

        except requests.exceptions.ConnectionError:
            st.error("Could not establish connection to the server.")
            st.info("If the server has been inactive, Render may take up to 60 seconds to wake up.")
            return None

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return None
