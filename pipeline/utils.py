from datetime import datetime,timedelta
import os
from config import db_path, occupation_field_dict

# Returns X past days since datetime.now() in a list format
# 60 days for new run and 
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


def make_params_list(day_range):
    from datetime import timedelta
    day_list = get_past_days(day_range)
    params_list = []
    # print("Building params list...")
    for field_name, field_code in occupation_field_dict.items():
        # print(f"Occupation field {field_name}:")
        for day in day_list:
            # print(f"{day}")
            tomorrow = day + timedelta(days=1)
            params = {
                "occupation-field": field_code,
                "published-before": tomorrow.strftime("%Y-%m-%dT00:00:00"),
                "published-after": day.strftime("%Y-%m-%dT00:00:00"),
                "limit": 100,
                "offset": 0,
            }
            params_list.append(params)
    return params_list


def delete_duckdb_file():
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Deleted DuckDB file at {db_path}")
    else:
        print(f"⚠️ DuckDB file not found at {db_path}, nothing to delete.")