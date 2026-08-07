import streamlit as st
import pandas as pd
import db_helpers as db
from pathlib import Path
from supabase import create_client, Client

# Connecting to supabase
conn = db.get_supabase_client()

# Gaining access to the documents folder
ROOT = Path(__file__).parents[1]
schema_png_path = ROOT/"files"/"PNG"/"Schmid Survey (1).png"

st.title("Database page 💾")

st.markdown("""
Welcome to the database page!

This system uses **SQLite** to efficiently store, structure, and manage survey responses exported from **Qualtrics**. 

**Key Objectives:**
* **Scalability:** Easily ingest and organize future survey runs within a unified schema.
* **Tableau Ready:** Automatically format and standardize dynamic survey responses for seamless visualization and reporting.
""")

st.subheader("🔀 Database Schema")

if schema_png_path.is_file():
    st.image(
        str(schema_png_path),
        caption = "SQLite database schema for storing of qualtrics survey data",
        use_container_width = True
    )
else:
    st.error(f"Could not find PDF file at {schema_png_path}")

# Let the user upload csv file containing Qualtrics data
st.subheader("📂 Upload your Qualtrics here: ")
uploaded_file = st.file_uploader("Upload SQLite file", type = "csv")

if uploaded_file is not None:

    survey_name = st.text_input("Enter the survey name: ")
    survey_date = st.date_input("Enter the date the survey was made: ")

    survey_id = db.insert_survey_info(survey_name, survey_date)
