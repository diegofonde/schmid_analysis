import streamlit as st
import pandas as pd
import db_helpers as db
from pathlib import Path
from supabase import create_client, Client

# Connecting to supabase
conn = st.session_state.supabase

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

tab1, tab2, tab3 = st.tabs([
    "Uploading raw survey data",
    "Obtaining answers to be cleaned",
    "Uploading clean answers"
])

with tab1:
    
    # Let the user upload csv file containing Qualtrics data
    st.subheader("📂 Upload your Qualtrics survey here: ")

    uploaded_file = st.file_uploader("Upload csv file", type = "csv")

    if uploaded_file is not None:

        uploaded_df = pd.read_csv(uploaded_file)
        
        survey_name = st.text_input("Enter the survey name: ")
        survey_date = st.date_input("Enter the date the survey was made: ")

        question_list = uploaded_df.iloc[:, 15:].columns.to_list()
        
        st.write("Select the questions for cleaning: ")
        selected_columns = st.multiselect(
            label = "Select your questions",
            options = question_list,
        )

        if st.button("Enter survey details"):

            st.session_state["selected_columns"] = selected_columns

            # Inserting details into the survey table
            survey_id = db.insert_survey_info(conn, survey_name, survey_date)
            st.session_state["survey_id"] = survey_id
            st.success(f"Uploading information for {survey_id}")

            responded_map, response_map = db.insert_respondant(conn, uploaded_df, survey_id)
            st.session_state["responded_map"] = responded_map
            st.success(f"Uploaded {len(responded_map)} responders")

            question_map = db.insert_question(conn, uploaded_df, survey_id)
            st.session_state["question_map"] = question_map
            st.success(f"Uploaded {len(question_map)} questions")

            responses = db.insert_responses(conn, uploaded_df, question_map, responded_map, response_map, selected_columns)
            st.success(f"Uploaded {len(responses)} responses")

            st.session_state["survey_uploaded"] = True





            
        
