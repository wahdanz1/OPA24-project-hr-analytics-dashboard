import dlt
from datetime import timedelta
from resources import jobsearch_resource
from utils import delete_duckdb_file, get_past_days, make_params_list

# To be able to import config.py and access its variables
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import variables from config.py
from config import db_path, table_name


# ---------- PIPELINE FUNCTIONS ----------
# Creates a pipeline 
def create_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name = "job_ads_pipeline",
        destination = dlt.destinations.duckdb(str(db_path)),
        dataset_name ="staging",
    )
    return pipeline

# Creates And Runs a pipeline
def run_pipeline(table_name , is_first_time:bool):
    pipeline = create_pipeline()
    if is_first_time:
        day_range = 60
        delete_duckdb_file()
        print("Creating new pipeline...")
    else:
        day_range = 2 
        print("Updating pipeline...")

    params_list = make_params_list(day_range)
    print(f"Fetching data...")
    pipeline.run(
        jobsearch_resource(params_list=params_list),
        table_name=table_name
    )

    print("Completed running the pipeline!")

# --- For testing purposes ---
if __name__ == "__main__":
    print("Running pipeline...")
    run_pipeline(table_name,is_first_time=False)
