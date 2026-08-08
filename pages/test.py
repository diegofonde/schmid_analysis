import streamlit as st

conn = st.session_state.supabase

st.title("Testing page")

st.file_uploader("Testing how to upload csv file into supbase")