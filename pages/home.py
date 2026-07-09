import streamlit as st
import requests
from datetime import datetime

GIT_HUB_REPO_OWNER = "diegofonde"
GIT_HUB_REPO_NAME = "schmid_analysis"

# Helper function to get commit messages from GitHub
# Function is ensured to only get updates commit messages from GitHub using API every 10 minutes 
@st.cache_data(ttl=600) 
def fetch_git_commit(owner, repo, max_commits = 5): 
    """Fetch latest Git commits"""

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"per_page": max_commits}

    try:
        response = requests.get(url = url)

        if response.status_code == 200: # Successful retrieval
            return response.json()
        elif response.status_code == 403:
            return "rate_limited"
        else:
            return None
    except Exception:
        return None


st.title("Home🏠")
st.header("Welcome to the home page!")

st.markdown("""
This webapp was created with the goal of long term analysis for schmid survey data!

Orginally my role as a Student Assistant started off simple data cleaning and analysis using excel. However, as I continued with the role I wanted to find more ways to utilize my skills and increase productivity leading to the culmination of this project!

### Features include:
1. **📊Page Dedicated for Dashboard:** View macro-level metrics and trends instantly.
2. **📲Clustering Algorithm:** Access the machine learning pipeline to segment profiles.
            
This webapp is still a WIP, and developments are ongoing.

_All features are created by Diego Fondevilla under Kate Hill's supervision :))
""")

st.write("---")
st.subheader("🚀 Live update feed")
st.markdown("""
Showcasing real-time respository updates synchronized directly via GitHub API
            """)

commits = fetch_git_commit(GIT_HUB_REPO_OWNER, GIT_HUB_REPO_NAME)

if commits == "rate_limited":
    st.info("🔄 Update feed temporalily sleeping to respect GitHub API rate limites.")
elif commits:
    for commit in commits: # For loop used to get every individual commit message
        commit_info = commit['commit']
        author_name = commit_info['author']['name']
        date_info = commit_info['author']['date']
        message = commit_info['message']
        
        clean_message = message.split('\n')[0]

        cleaned_date = datetime.strptime(date_info, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y • %I:%M %p")

        with st.container():
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown(f"**📅{cleaned_date.split(' • ')[0]}**")
                st.caption(f"**🕒{cleaned_date.split(' • ')[1]}")

            with col2:
                st.markdown(f"#####{clean_message}")
                st.markdown(f"🛠️ **Developer:** {author_name}")
            st.write("")
            st.markdown("<hr style='margin: 0px 0px 15px 0px; opacity: 0.25;'>", unsafe_with_html = True) # Diviver
else:
    st.caption("Unable to load the live commit feed at this time. Repository may be private or offline.")


