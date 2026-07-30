import streamlit as st
import pandas as pd

st.title("Database page 💾")

st.markdown("""
Welcome to the database page!

This system uses **SQLite** to efficiently store, structure, and manage survey responses exported from **Qualtrics**. 

**Key Objectives:**
* **Scalability:** Easily ingest and organize future survey runs within a unified schema.
* **Tableau Ready:** Automatically format and standardize dynamic survey responses for seamless visualization and reporting.
""")

st.subheader("🔀 Database Schema")
