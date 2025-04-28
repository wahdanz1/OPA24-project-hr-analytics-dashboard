import dlt
from resources import jobsearch_resource
from datetime import datetime,timedelta

# To be able to import config.py and access its variables
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import variables from config.py
from config import db_path, table_name, occupation_field_list,municipalities,working_directory


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
            
            day_list = get_dates_to_check()
            for day in day_list:
                tomorrow = day + timedelta(days=1)

                params = {
                    "occupation-field": field,
                    "published-before":tomorrow.strftime("%Y-%m-%dT00:00:00"),
                    "published-after":day.strftime("%Y-%m-%dT00:00:00"),
                    "limit": 100,
                    "offset": 0,
                }
                print(f"occupation-field: {field} todays date: {day}")
                pipeline.run(
                    jobsearch_resource(params=params),
                    table_name=table_name
                )
    print("Completed running the pipeline!")
def get_dates_to_check():
    today = datetime.now()
    first_listing = today - timedelta(days=12)
    return_list = []
    for i in range(12):
         day_to_test = first_listing + timedelta(days = i)
         return_list.append(day_to_test)
         

    return return_list


#.strftime("%Y-%m-%d")

    print("Completed Filter using Datetime")

# --- For testing purposes ---
if __name__ == "__main__":
    get_dates_to_check()
    #print("Running pipeline...")
    run_pipeline(table_name)