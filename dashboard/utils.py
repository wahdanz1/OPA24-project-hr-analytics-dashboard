import pandas as pd
import streamlit as st
from pipeline.db import DuckDBConnection
from config import db_path

def fetch_data_from_db(query: str) -> pd.DataFrame:
    with DuckDBConnection(db_path) as conn:
        return conn.query(query)
    

# Set the occupation field name based on the selected occupation field
def set_occupation_field_name(occupation_field_choices):
    mapping = {
        "Administration, finance & law": "Administration, ekonomi, juridik",
        "Sales & marketing": "Försäljning, inköp, marknadsföring",
        "Healthcare": "Hälso- och sjukvård",
    }
    
    if "All fields" in occupation_field_choices or not occupation_field_choices:
        return None  # No filtering
    
    return [mapping[choice] for choice in occupation_field_choices if choice in mapping]

# Function for building the WHERE clause for SQL queries, based on the selected occupation field
def build_where_clause() -> str:
    # Check if the occupation_field is "All fields" and set it to None if so
    occupation_field_choices = st.session_state.get("occupation_field_choice", [])
    occupation_field_names = set_occupation_field_name(occupation_field_choices)

    # Based on the occupation_field_names, set the WHERE clause for the SQL query
    if occupation_field_names is None:
        where_clause = ""
    else:
        # Create a list of quoted strings for SQL IN clause
        name_list = ", ".join(f"'{name}'" for name in occupation_field_names)
        where_clause = f"WHERE occupation_field IN ({name_list})"
    
    return where_clause