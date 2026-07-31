import streamlit as st
import pandas as pd
from pathlib import Path

# Gaining access to the documents folder
ROOT = Path(__file__).parents[1]
schema_pdf_path = ROOT/"files"/"PDF"/"Scmid Survey.pdf"

st.title("Database page 💾")

st.markdown("""
Welcome to the database page!

This system uses **SQLite** to efficiently store, structure, and manage survey responses exported from **Qualtrics**. 

**Key Objectives:**
* **Scalability:** Easily ingest and organize future survey runs within a unified schema.
* **Tableau Ready:** Automatically format and standardize dynamic survey responses for seamless visualization and reporting.
""")

st.subheader("🔀 Database Schema")

if schema_pdf_path.is_file():
    st.pdf(schema_pdf_path)
else:
    st.error(f"Could not find PDF file at {schema_pdf_path}")
