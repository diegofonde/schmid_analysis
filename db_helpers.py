import streamlit as st
import pandas as pd
import secrets
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    
    # Initializes and caches the Supabase client using Streamlit secrets.

    if "supabase" not in st.secrets:
        raise KeyError("Missing [supabase] configuration in st.secrets.")
    
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def insert_survey_info(connection, survey_name, survey_date):
    new_survey = {
        "title": survey_name,
        "date": str(survey_date)
    }

    response = connection.table("surveys").insert(new_survey).execute()

    return response[0]["survey_id"]





