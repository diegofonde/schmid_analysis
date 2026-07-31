import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# Gaining access to the documents folder
ROOT = Path(__file__).parents[1]
schema_png_path = ROOT/"files"/"PNG"/"Schmid Survey (1).png"

st.title("Database page 💾")

st.markdown("""
Welcome to the database page!

This system uses **SQLite** to efficiently store, structure, and manage survey responses exported from **Qualtrics**. 

**Key Objectives:**
* **Scalability:** Easily ingest and organize future survey runs within a unified schema.
* **Tableau Ready:** Automatically format and standardize dynamic survey responses for seamless visualization and reporting.
""")

st.subheader("🔀 Database Schema")

if schema_png_path.is_file():
    st.image(
        str(schema_png_path),
        caption = "SQLite database schema for storing of qualtrics survey data",
        use_container_width = True
    )
else:
    st.error(f"Could not find PDF file at {schema_png_path}")

# Let the user upload SQLite file
st.subheader("📂 Upload your SQLite file here: ")
uploaded_file = st.file_uploader("Upload SQLite file", type = ["db", "sqlite", "sqlite3"])

if uploaded_file is not None:
    st.write("Hurray")
