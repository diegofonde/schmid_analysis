import streamlit as st
import pandas as pd
import db_helpers as db

conn = st.session_state.supabase

st.title("Testing page")

upload = st.file_uploader("Testing how to upload csv file into supbase")

if upload is not None: 

    if st.button("Upload file"):

        upload_df = pd.read_csv(upload)

        st.write("RAW ROW 0 DATE STRING:", repr(upload_df['Recorded Date'].iloc[0]))
        st.stop()