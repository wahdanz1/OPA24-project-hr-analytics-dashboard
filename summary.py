import streamlit as st
import pandas as pd
from dashboard.utils import fetch_data_from_db, get_sidebar_filters

def summary_page():
    st.header("Summary", divider=True)

    occupation_fields = get_selected_occupation_fields()
    st.markdown(f"**Selected Occupation Fields:**  {occupation_fields}")
    display_kpis()




    


def display_kpis():
    
    selected_posted = get_jobs_posted_selected_period()
    st.metric(label="Jobs Posted in Selected Period", value=selected_posted, delta=None)






# Returns the number of jobs posted in the selected period
def get_jobs_posted_selected_period():
    # Get the sidebar filters
    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    # Query to get the number of jobs posted in the selected period
    query = f"""
        SELECT COUNT(*) AS jobs_posted
        FROM marts.mart_occupation_trends_over_time
        WHERE publication_date BETWEEN (NOW() - INTERVAL {end_day} DAY)
            AND (NOW() - INTERVAL {start_day} DAY)
            AND occupation_field IN ({name_string})
    """
    df = fetch_data_from_db(query)
    return df['jobs_posted'].values[0]


# Returns the selected occupation fields from the sidebar
# and formats them for display
def get_selected_occupation_fields():
    # Get the sidebar filters
    name_string, limit_value, start_day, end_day = get_sidebar_filters()
    occupation_list = name_string.split(",")
    # Remove Fnutts from the list
    formatted_list = [x.strip("'") for x in occupation_list]
    # Format the list with bold text
    formatted_string = ", ".join([f"{x}" for x in formatted_list])
    # Return the formatted string
    return formatted_string