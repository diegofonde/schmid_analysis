import streamlit as st
import pandas as pd
from pipelines import data_cleaner_helpers as dc
from pipelines import db_helpers as db
from pipelines import model_helpers as mh

conn = st.session_state.supabase

st.title("Testing Page")

unclean_student_list = db.get_uncleaned_answers(conn)
clean_student_list = dc.clean_raw_data(unclean_student_list)
submission = db.upload_cleaned_answers(conn, clean_student_list)
st.success(f"Submitted {submission} clean answers.")

response = conn.table("model_input").select("*").execute()
raw_json = response.data
model_input_df = pd.DataFrame(raw_json)
st.dataframe(model_input_df, use_container_width=True)

with st.spinner:
    predictions = mh.predict(raw_json)

st.json(predictions)



