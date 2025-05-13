import streamlit as st
import pandas as pd
from dashboard.utils import fetch_data_from_db, get_sidebar_filters

def summary_page():
    st.header("Summary", divider=True)

    occupation_fields = get_selected_occupation_fields()
    st.markdown(f"**Selected Occupation Fields:**  {occupation_fields}")
    
    
    display_kpis()




    


def display_kpis():
    occupation_employers = get_occupation_with_most_unique_employers()
    st.metric(label="Occupation with Most Unique Employers", value=occupation_employers)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_posted = get_jobs_posted_selected_period()
        st.metric(label="Jobs Posted within selected parameters", value=selected_posted)

    with col2:
        experience_percentage = get_experience_percentage()
        st.metric(label="Percentage of jobs requiring experience", value=f"{experience_percentage} %")
    with col3:
        pass

        
    display_dataframes()

def display_dataframes():
    col1,col2 = st.columns([1,1])
    

    
    with col1:
        top_occupations = get_top_occupations()
        st.subheader("Top 5 Occupations")
        st.dataframe(top_occupations, use_container_width=True,hide_index=True)

        
        avg_vacancy_df = average_vacancies_per_job_ad()
        st.subheader("Employers with Highest Avg. Vacancies per Ad")
        st.dataframe(avg_vacancy_df, use_container_width=True,hide_index=True)


    with col2:
        st.subheader("Jobs requiring little to no experience")
        least_experience_occupation_df = get_top_5_least_experience_occupations()
        st.dataframe(least_experience_occupation_df, use_container_width=True,hide_index=True)

        st.subheader("Occupations with Most Unique Employers")
        top_unique_employer_occupations = get_top_5_occupations_by_unique_employers()
        st.dataframe(top_unique_employer_occupations, use_container_width=True, hide_index=True)



################################################
#   Methods that return values for the KPIs    #
################################################

# Returns the number of jobs posted in the selected period
def get_jobs_posted_selected_period():
    name_string, _, start_day, end_day = get_sidebar_filters()
    query = f"""
        SELECT COUNT(*) AS jobs_posted
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL {end_day} DAY)
          AND (NOW() - INTERVAL {start_day} DAY)
          AND occupation_field IN ({name_string})
    """
    df = fetch_data_from_db(query)
    return df['jobs_posted'].values[0]


def get_experience_percentage() -> float:
    name_string, _, start_day, end_day = get_sidebar_filters()

    query = f"""
        SELECT 
            ROUND(100.0 * COUNT(*) FILTER (WHERE experience_required = TRUE) / NULLIF(COUNT(*), 0), 2)
            AS percent_with_experience_required
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
          AND (NOW() - INTERVAL '{start_day} day')
          AND occupation_field IN ({name_string});
    """
    result = fetch_data_from_db(query)
    return float(result.iloc[0, 0]) if not result.empty and result.iloc[0, 0] is not None else 0.0


def average_vacancies_per_job_ad():
    name_string, _, start_day, end_day = get_sidebar_filters()

    query = f"""
        SELECT 
            employer_name,
            ROUND(AVG(NULLIF(vacancies, 0)), 2) AS avg_vacancies_per_job_ad,
            COUNT(*) AS total_ads
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
          AND (NOW() - INTERVAL '{start_day} day')
          AND occupation_field IN ({name_string})
          AND employer_name IS NOT NULL
          AND vacancies BETWEEN 1 AND 50
        GROUP BY employer_name
        HAVING COUNT(*) >= 3
        ORDER BY avg_vacancies_per_job_ad DESC
        LIMIT 5;
    """
    df = fetch_data_from_db(query)
    return df

def get_occupation_with_most_unique_employers() -> str:
    name_string, _, start_day, end_day = get_sidebar_filters()

    query = f"""
        SELECT 
            occupation,
            COUNT(DISTINCT employer_name) AS unique_employer_count
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
          AND (NOW() - INTERVAL '{start_day} day')
          AND occupation_field IN ({name_string})
          AND employer_name IS NOT NULL
        GROUP BY occupation
        ORDER BY unique_employer_count DESC
        LIMIT 1;
    """

    df = fetch_data_from_db(query)
    if df.empty:
        return "No data"

    occ = df.iloc[0]["occupation"]
    count = df.iloc[0]["unique_employer_count"]
    return f"{occ} ({count} employers)"

def get_top_5_occupations_by_unique_employers() -> pd.DataFrame:
    name_string, _, start_day, end_day = get_sidebar_filters()

    query = f"""
        SELECT 
            occupation,
            COUNT(DISTINCT employer_name) AS unique_employer_count
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
          AND (NOW() - INTERVAL '{start_day} day')
          AND occupation_field IN ({name_string})
          AND employer_name IS NOT NULL
        GROUP BY occupation
        ORDER BY unique_employer_count DESC
        LIMIT 5;
    """

    df = fetch_data_from_db(query)
    return df if not df.empty else pd.DataFrame(columns=["occupation", "unique_employer_count"])

def get_top_occupations():
    name_string, _, start_day, end_day = get_sidebar_filters()

    query = f"""
        SELECT occupation, SUM(vacancies) AS total_vacancies
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
          AND (NOW() - INTERVAL '{start_day} day')
          AND occupation_field IN ({name_string})
        GROUP BY occupation
        ORDER BY total_vacancies DESC
        LIMIT 5;
    """
    df = fetch_data_from_db(query)
    return df


def get_top_5_least_experience_occupations() -> pd.DataFrame:
    name_string, _, start_day, end_day = get_sidebar_filters()

    query = f"""
        SELECT 
            occupation,
            SUM(vacancies) AS total_vacancies
        FROM marts.mart_summary
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
    return result if not result.empty else pd.DataFrame(columns=["occupation", "total_vacancies"])





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