import sqlite3
import tempfile

def get_connection(uploaded_file):
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".db") as tmp_file: # This is important since st.file_uploader() stores memory in the RAM, but in order to connect sqlite3 needs a file path
            tmp_file.write(uploaded_file.getvalue())
            temp_db_path = tmp_file.name
    
    conn = sqlite3.connect(temp_db_path)

