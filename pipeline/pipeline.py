import dlt
from resources import jobsearch_resource

# To be able to import config.py and access its variables
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import variables from config.py
from config import db_path, table_name, occupation_field_list


# ---------- PIPELINE FUNCTIONS ----------
# Creates a pipeline 
def create_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name = "hr_data_pipeline",
        destination = dlt.destinations.duckdb(str(db_path)),
        dataset_name ="staging",
    )
    return pipeline

# Creates And Runs a pipeline
def run_pipeline(table_name):
    pipeline = create_pipeline()

    # Loop through each occupation field in the list
    for field in occupation_field_list:
        params = {
            "occupation-field": field,
            "limit": 100,
            "offset": 0,
        }
        print(params)

        pipeline.run(
            jobsearch_resource(params=params),
            table_name=table_name
        )
    
    print("Completed running the pipeline!")


# --- For testing purposes ---
if __name__ == "__main__":
    print("Running pipeline...")
    run_pipeline(table_name)