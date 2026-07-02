import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title = "Schmid College Student Analysis", layout = "wide")

home_page = st.Page("pages/home.py", title = "Home", icon = "🏠", default = True)
dashboard_page = st.Page("pages/dashboard.py", title = "Interactive Dashboard", icon = "📊", default = False)
model_page = st.Page("pages/model.py", title = "PAM Model", icon = "📲", default = False)

pg = st.navigation([home_page, dashboard_page, model_page])
pg.run()

# st.title("Schmid Student Segmentation Tool")
# st.markdown("User interfact for viewing dashboards and clustering students")

# API_URL =  "http://0.0.0.0:10000"

# st.sidebar.header("Navigation")