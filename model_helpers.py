import pandas as pd
import requests
import streamlit as st

API_URL_PREDICT =  "https://schmid-student-segmentation-api.onrender.com/predict" # API URL for API prediction hosted in Render
API_URL_MEDOIDS =  "https://schmid-student-segmentation-api.onrender.com/medoids" # API URL for API medoids hosted in Render

def predict(student_list):

    payload = {"students": student_list}

    with st.spinner("Calculating..."):

        try:

            response = requests.post(API_URL_PREDICT, json = payload, timeout = 90)

            if response.status_code == 200:
        

                # Putting API response back into a dataframee
                predictions = response.json().get("Predictions", [])

                new_predictions = [
                    {
                        "respondent_id": student_list[i].get('respondent_id'),
                        "cluster_id": pred.get('group'),                    
                    }
                    for i, pred in enumerate(predictions)
                ]

                return new_predictions
            
            # Explicit error handling UI
            return f"API Error {response.status_code}: {response.text}"
            
        except requests.exceptions.Timeout:
            return "Request timed out. Render free-tier web services may take up to 60 seconds to wake up."

        except requests.exceptions.ConnectionError:
            return "Could not establish connection to the server. Render may be sleeping."

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
