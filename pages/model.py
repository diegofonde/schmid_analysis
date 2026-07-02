import streamlit as st
import pandas as pd
import requests

st.title("PAM Clustering Model")
st.markdown("Here is the page dedicated to clustering students based on the inputted dataset!")

API_URL =  "http://0.0.0.0:10000" # API URL for API being hosted in Render

st.subheader("📂 Upload your dataset here: ")
st.file_uploader("Upload a CSV file", type = ["csv"])

