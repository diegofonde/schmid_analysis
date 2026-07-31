import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# Gaining access to the documents folder
ROOT = Path(__file__).parents[1]
schema_pdf_path = ROOT/"files"/"PDF"/"Schmid Survey.pdf"

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
    with open(schema_pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html = True)
else:
    st.error(f"Could not find PDF file at {schema_pdf_path}")
