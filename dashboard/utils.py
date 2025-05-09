import pandas as pd
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