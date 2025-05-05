from datetime import datetime,timedelta
import os
from config import db_path

# Returns past 12 days in datetime format
def get_all_days():
    today = datetime.now()
    first_listing = today - timedelta(days=183) # 183 = 6 months, used for inital pipeline-run
    return_list = []
    for i in range(183):
        day_to_test = first_listing + timedelta(days = i)
        return_list.append(day_to_test)
        
    print("Completed Filter using Datetime")
    return return_list

# Returns days from last update until now 
def get_days_since_update(last_update_day:datetime):
    today = datetime.now()
    days_to_check = (today-last_update_day).days
    return_list = []
    for i in range(days_to_check):
        day_to_test = last_update_day + timedelta(days = i)
        return_list.append(day_to_test)
    return return_list
    


def delete_duckdb_file():
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Deleted DuckDB file at {db_path}")
    else:
        print(f"⚠️ DuckDB file not found at {db_path}, nothing to delete.")