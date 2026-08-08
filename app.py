import streamlit as st
import db_helpers as db
from supabase import create_client, Client

# Connecting to supabase which will be shared by the whole webapp
if "supabase" not in st.session_state:
    st.session_state.supabase = db.get_supabase_client()

st.set_page_config(page_title = "Schmid College Student Analysis", layout = "wide")

home_page = st.Page("pages/home.py", title = "Home", icon = "🏠", default = True)
dashboard_page = st.Page("pages/dashboard.py", title = "Interactive Dashboard", icon = "📊", default = False)
model_page = st.Page("pages/model.py", title = "PAM Model", icon = "📲", default = False)
database_page = st.Page("pages/database.py", title = "Database", icon = "💾", default = False)
test_page = st.Page("pages/test.py", title = "Test", default = False )

pg = st.navigation([home_page, dashboard_page, model_page, database_page])
pg.run()