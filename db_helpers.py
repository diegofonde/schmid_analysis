import streamlit as st
import pandas as pd
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    
    # Initializes and caches the Supabase client using Streamlit secrets.

    if "supabase" not in st.secrets:
        raise KeyError("Missing [supabase] configuration in st.secrets.")
    
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

# Function for inserting survey information into supabase
def insert_survey_info(connection, survey_name, survey_date):
    new_survey = {
        "title": survey_name,
        "date": str(survey_date)
    }

    response = connection.table("surveys").insert(new_survey).execute()

    return response.data[0]["survey_id"]

# Function for inserting the respondants into supabase
def insert_respondant(connection, df):

    # Obtain needed informataion from the dataframe
    respondents_df = df[['Recipient Email', 'Recipient First Name', 'Recipient Last Name']].drop_duplicates(
        subset = ['Recipient Email'],
        keep = 'last'
    )

    respondents_df = respondents_df.rename(
        columns = {
            'Recipient Email': 'email',
            'Recipient First Name': 'first_name',
            'Recipient Last Name': 'last_name'
        }
    )

    # Converting dataframe into a list of dictionaries with each dictionary representing a row
    new_respondents = respondents_df.to_dict(orient = "records")

    response = connection.table("respondents").insert(new_respondents).execute()

    # Creates a dictionary for other tables that can easily access the respondent id based on the email
    respondent_map = {row["email"] : row["respondent_id"] for row in response.data}

    return respondent_map

def insert_question(connection, df, survey_id):

    df_questions = df.iloc[:, 15:]

    # Obtaining the questions from the columns of the dataframe into a list
    questions_list = df_questions.columns.tolist()

    new_questions = [
        {
            "question_text": question_text,
            "survey_id": survey_id
        }
        for question_text in questions_list
    ]

    response = connection.table("questions").insert(new_questions).execute()

    question_map = {row["question_text"]: row["question_id"] for row in response.data}

    return question_map







