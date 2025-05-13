import streamlit as st
import pandas as pd
from dashboard.utils import fetch_data_from_db, get_sidebar_filters

def summary_page():
    st.header("Summary", divider=True)

    occupation_fields = get_selected_occupation_fields()
    st.markdown(f"**Selected Occupation Fields:**  {occupation_fields}")
    
    
    display_kpis()




    


def display_kpis():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_posted = get_jobs_posted_selected_period()
        st.metric(label="Jobs Posted within selected parameters", value=selected_posted)

    with col2:
        experience_percentage = get_experience_percentage()
        st.metric(label="Experience Required (%)", value=f"{experience_percentage} %")
    with col3:
        pass
        
        

        

    display_dataframes()

def display_dataframes():
    col1,col2 = st.columns([1,1])
    

    
    with col1:
        top_occupations = get_top_occupations()
        st.subheader("Top 5 Occupations")
        st.dataframe(top_occupations, use_container_width=True)
    with col2:
        st.subheader("Jobs requiring little to no experience")
        least_experience_occupation_df = get_top_5_least_experience_occupations()
        st.dataframe(least_experience_occupation_df, use_container_width=True)
    # Display the top 5 occupations



################################################
#   Methods that return values for the KPIs    #
################################################

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


def get_top_occupations():
    # Get the sidebar filters
    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    # Query to get the top occupations
    query = f"""
        SELECT d.occupation, SUM(vacancies) AS total_vacancies
        FROM refined.fct_job_ads f
        JOIN refined.dim_occupation d ON f.occupation_id = d.occupation_id
        WHERE publication_date BETWEEN (NOW() - INTERVAL {end_day} DAY)
        AND (NOW() - INTERVAL {start_day} DAY)
        AND occupation_field IN ({name_string})
        GROUP BY d.occupation
        ORDER BY total_vacancies DESC
        LIMIT 5;

    """
    df = fetch_data_from_db(query)
    return df

def get_experience_percentage() -> float:
    # Get the sidebar filters
    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    # Format occupation_field list for SQL
    if isinstance(name_string, list):
        name_string = ', '.join(f"'{name}'" for name in name_string)

    # Query directly from the mart
    query = f"""
        SELECT 
        ROUND(100.0 * COUNT(*) FILTER (WHERE experience_required = TRUE) / NULLIF(COUNT(*), 0),2) AS percent_with_experience_required
        FROM marts.mart_occupation_trends_over_time
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
                                   AND (NOW() - INTERVAL '{start_day} day')
        AND occupation_field IN ({name_string});
    """
    result = fetch_data_from_db(query)

    if result.empty or result.iloc[0, 0] is None:
        print("No data found for the given filters.")
        return 0.0
    return float(result.iloc[0, 0])

def get_top_5_least_experience_occupations() -> pd.DataFrame:
    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    # Format occupation_field list for SQL
    if isinstance(name_string, list):
        name_string = ', '.join(f"'{name}'" for name in name_string)

    query = f"""
        SELECT 
            occupation,
            SUM(vacancies) AS total_vacancies
        FROM marts.occupation_trends_over_time
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
                                   AND (NOW() - INTERVAL '{start_day} day')
          AND occupation_field IN ({name_string})
        GROUP BY occupation
        HAVING ROUND(
            100.0 * COUNT(*) FILTER (WHERE experience_required = TRUE) / NULLIF(COUNT(*), 0),
            2
        ) < 25
        ORDER BY total_vacancies DESC
        LIMIT 5;
    """

    result = fetch_data_from_db(query)

    if result.empty:
        return pd.DataFrame(columns=["occupation", "experience_percentage", "total_vacancies"])

    return result






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