from datetime import datetime,timedelta
import os
from config import db_path

# Returns X past days since datetime.now() in a list format
# 183 days for new run and 
# X days where X is time since last update
def get_past_days(past_days : int):
    today = datetime.now()
    first_listing = today - timedelta(days=past_days) 
    return_list = []
    for i in range(past_days+1): 
        day_to_test = first_listing + timedelta(days = i)
        return_list.append(day_to_test)
        
    print(f"Retrieved a list with the past {past_days} days")
    return return_list


    


def delete_duckdb_file():
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Deleted DuckDB file at {db_path}")
    else:
        print(f"⚠️ DuckDB file not found at {db_path}, nothing to delete.")