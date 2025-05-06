import pandas as pd
from pipeline.db import DuckDBConnection
from config import db_path

def fetch_data_from_db(query: str) -> pd.DataFrame:
    with DuckDBConnection(db_path) as conn:
        return conn.query(query)