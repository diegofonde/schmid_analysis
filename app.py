import streamlit as st

st.set_page_config(page_title = "Schmid College Student Analysis", layout = "wide")

home_page = st.Page("pages/home.py", title = "Home", icon = "🏠", default = True)
dashboard_page = st.Page("pages/dashboard.py", title = "Interactive Dashboard", icon = "📊", default = False)
model_page = st.Page("pages/model.py", title = "PAM Model", icon = "📲", default = False)
database_page = st.Page("pages/database.py", title = "Database", icon = "💾", default = False)

pg = st.navigation([home_page, dashboard_page, model_page])
pg.run()