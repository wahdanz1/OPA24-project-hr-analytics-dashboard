from datetime import datetime,timedelta

# Returns past 12 days in datetime format
def get_all_days():
    today = datetime.now()
    first_listing = today - timedelta(days=12)
    return_list = []
    for i in range(12):
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
    