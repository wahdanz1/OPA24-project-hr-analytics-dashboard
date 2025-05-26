import dlt
from resources import jobsearch_resource
from datetime import datetime,timedelta
import utils

# To be able to import config.py and access its variables
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import variables from config.py
from config import db_path, table_name, occupation_field_dict


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
        day_list = utils.get_past_days(60)
        utils.delete_duckdb_file()
        print("Creating new pipeline...")
    else:
        day_list = utils.get_past_days(3) 
        print("Updating pipeline...")

    # Loop through each occupation field in the list
    for field_name,field_code in occupation_field_dict.items():
            print(f"Loading {field_name}")
            for day in day_list:
                tomorrow = day + timedelta(days=1)

                params = {
                    "occupation-field": field_code,
                    "published-before":tomorrow.strftime("%Y-%m-%dT00:00:00"),
                    "published-after":day.strftime("%Y-%m-%dT00:00:00"),
                    "limit": 100,
                    "offset": 0,
                }
                print(f"Loading {day}")
                pipeline.run(
                    jobsearch_resource(params=params),
                    table_name=table_name
                )
    print("Completed running the pipeline!")

# --- For testing purposes ---
if __name__ == "__main__":
    print("Running pipeline...")
    run_pipeline(table_name,is_first_time=False)