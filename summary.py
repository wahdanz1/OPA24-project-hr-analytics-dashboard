import streamlit as st
import pandas as pd
from dashboard.utils import fetch_data_from_db, get_sidebar_filters

def summary_page():
    st.header("Summary", divider=True)
    everything_method()

    pass

def everything_method():

    display_kpis()

    pass

def display_kpis():
    # Fetch data from the database
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

