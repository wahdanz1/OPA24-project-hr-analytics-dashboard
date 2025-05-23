import duckdb as ddb
import pandas as pd

# --- Database connection class ---
class DuckDBConnection:
    """Context manager for DuckDB connection."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = ddb.connect(str(self.db_path))
        return self
    
    def query(self, query, params=None) -> pd.DataFrame:
        """Execute a query with optional parameters and return the result."""
        try:
            if params: # If parameters are provided, use them in the query
                return self.conn.execute(query, params).df()
            else: # If no parameters, execute the query directly
                return self.conn.execute(query).df()
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()  # Return an empty DataFrame if there's an error
    
    def execute(self, query, params=None): # Execute a non-select query
        """Execute a non-select query (e.g., CREATE TABLE, INSERT, etc.)"""
        try:
            if params:
                self.conn.execute(query, params)
            else:
                self.conn.execute(query)
        except Exception as e:
            print(f"Error executing command: {e}")

    def register_df(self, name: str, df: pd.DataFrame): # Register a DataFrame as a DuckDB temp table
        """Register a DataFrame as a DuckDB temp table."""
        self.conn.register(name, df)


    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()