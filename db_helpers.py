import streamlit as st
import numpy as np
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

    response = connection.table("surveys").insert(new_survey).select().execute()

    return response.data[0]["survey_id"]

# Function for inserting the respondants into supabase
def insert_respondant(connection, df, survey_id):

    # Removing duplicates from the dataframe in preparation for respondents and responses tables
    cleaned_df = df.drop_duplicates(
        subset = ['Recipient Email'],
        keep = 'last'
    )

    # Obtain needed informataion from the dataframe for respondents table
    respondents_df = cleaned_df[['Recipient Email', 'Recipient First Name', 'Recipient Last Name']]

    respondents_df = respondents_df.rename(
        columns = {
            'Recipient Email': 'email',
            'Recipient First Name': 'first_name',
            'Recipient Last Name': 'last_name'
        }
    )

    # Converting dataframe into a list of dictionaries with each dictionary representing a row
    new_respondents = respondents_df.to_dict(orient = "records")

    response = connection.table("respondents").upsert(new_respondents, on_conflict="email").select().execute()

    # Creates a dictionary for other tables that can easily access the respondent id based on the email
    respondent_map = {row["email"]: row["respondent_id"] for row in response.data}

    # Matches the respondent id based on the email
    responses_df = cleaned_df[['Recipient Email', 'Recorded Date']].copy()
    responses_df['respondent_id'] = responses_df['Recipient Email'].map(respondent_map)
    responses_df = responses_df.dropna(subset=['respondent_id'])

    clean_date_string = responses_df['Recorded Date'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

    parsed_date = pd.to_datetime(clean_date_string, format='mixed')

    responses_df['Recorded Date'] = parsed_date.dt.strftime('%Y-%m-%d %H:%M:%S')

    new_responses = [
        {
            "survey_id": str(survey_id),
            "respondent_id": str(row['respondent_id']),
            "submitted_at": row['Recorded Date']
        }

        for row in responses_df.to_dict(orient = 'records')
    ]

    response = connection.table("responses").insert(new_responses).select().execute()

    response_map = {row['respondent_id']: row['response_id'] for row in response.data}

    return respondent_map, response_map

def insert_question(connection, df, survey_id):

    df_questions = df.iloc[:, 17:]

    # Obtaining the questions from the columns of the dataframe into a list
    questions_list = df_questions.columns.tolist()

    new_questions = [
        {
            "question_text": question_text,
            "survey_id": survey_id,
            "position": pos
        }
        for pos, question_text in enumerate(questions_list, start = 1)
    ]

    response = connection.table("questions").insert(new_questions).select().execute()

    question_map = {row["question_text"]: row["question_id"] for row in response.data}

    return question_map

def insert_responses(connection, df, question_map, respondent_map, response_map):

    question_list = list(question_map.keys())
    question_list.append("Recipient Email")

    df_cleaned = df[question_list].copy()

    df_cleaned_long = df_cleaned.melt(
        id_vars = ['Recipient Email'],
        value_vars = list(question_map.keys()),
        var_name = 'Question',
        value_name = 'Answer'
    )

    new_answers = [
        {
            "question_id": question_map[row['Question']],
            "response_id": response_map[respondent_map[row['Recipient Email']]],
            "answer": str(row['Answer']),
            "clean_answer": "",
            "is_cleaned": 0
        }

        for row in df_cleaned_long.to_dict(orient = 'records')
    ]

    response = connection.table("answers").insert(new_answers).select().execute()

    return response.data

def uncleaned_answers(connection):

    response = (
            connection.table("answers")
            .select("answer_id, questions(question_text), answer, clean_answer" )
            .eq("clean_answer", "")
            .execute()
        )

    return response.data