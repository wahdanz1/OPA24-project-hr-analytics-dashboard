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
    
    if not occupation_field_choices:
        return None  # No filtering
    
    return [mapping[choice] for choice in occupation_field_choices if choice in mapping]

# Function for building the occupation name string, based on the selected occupation field(s)
def get_occupation_field_name_string():
    # Check if the occupation_field is empty and set it to None if so
    occupation_field_choices = st.session_state.get("occupation_field_choice", [])
    occupation_field_names = set_occupation_field_name(occupation_field_choices)

    # Based on the occupation_field_names, build the name_string with all occupation fields
    if occupation_field_names is None:
        name_string = "'Administration, ekonomi, juridik', 'Försäljning, inköp, marknadsföring','Hälso- och sjukvård'"
    else:
        # Create a string with the selected occupation fields
        name_string = ", ".join(f"'{name}'" for name in occupation_field_names)
    
    return name_string