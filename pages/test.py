import streamlit as st
from pipelines import data_cleaner_helpers as dc
from pipelines import db_helpers as db

conn = st.session_state.supabase

st.title("Testing Page")

unclean_student_list = db.get_uncleaned_answers(conn)
clean_student_list = dc.clean_raw_data(unclean_student_list)
submission = db.upload_cleaned_answers(conn, clean_student_list)
st.success(f"Submitted {submission} clean answers.")

