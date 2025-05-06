import pandas as pd
from pipeline.db import DuckDBConnection
from config import db_path

def get_distinct_occupations() -> pd.DataFrame:
    """Fetch distinct occupations per municipality from the database."""    
    query = f"""
        SELECT DISTINCT
        COUNT(o.occupation_id) AS distinct_occupations,
        e.workplace_municipality
        FROM refined.fct_job_ads ja
        
        JOIN refined.dim_employer e
            ON e.employer_id = ja.employer_id
        JOIN refined.dim_occupation o
            ON o.occupation_id = ja.occupation_id
        
        WHERE workplace_municipality IS NOT NULL

        GROUP BY e.workplace_municipality
        ORDER BY distinct_occupations DESC
        LIMIT 15
    """

    with DuckDBConnection(db_path) as conn:
        return conn.query(query)