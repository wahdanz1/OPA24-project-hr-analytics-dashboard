import streamlit as st
import pandas as pd
from .utils import fetch_data_from_db, get_sidebar_filters, display_dynamic_heading, wrap_label
from .plots import create_pie_chart

def summary_page():
    display_dynamic_heading()
    display_kpis_and_pie()
    display_dataframes()

# ---------- KPI & Pie-section ----------
def display_kpis_and_pie():
    occupation_employers = get_occupation_with_most_unique_employers()
    st.metric(label="Occupation with Most Unique Employers", value=occupation_employers)

    col1, col2 = st.columns(2)

    # First column - KPI's
    with col1:
        display_kpis()

    # Second column - Pie chart (occupational distribution)
    with col2:
        display_pie()

# ---------- KPI's ----------
def display_kpis():
    st.subheader("KPI's", divider=True)
    with st.container():
        selected_posted = get_jobs_posted_with_current_filters()
        st.metric(label="Jobs posted within selected parameters", value=selected_posted)

    with st.container():
        experience_percentage = round(get_experience_percentage())
        st.metric(label="Jobs requiring experience", value=f"{experience_percentage} %")

    with st.container():
        driver_license_percentage = round(get_driver_license_percentage())
        st.metric(label="Jobs requiring driver's license", value=f"{driver_license_percentage} %")

# ---------- Pie chart ----------
def display_pie():
    st.subheader("Occupational Distribution (2% or more)", divider=True)
    
    # Get the data for the pie chart
    data = get_occupational_distribution()

    data["wrapped_occupation"] = data["occupation"].apply(wrap_label)

    # Create and display the pie chart using Plotly
    fig = create_pie_chart(
        data,
        values="total_vacancies",
        names="wrapped_occupation",
        title=" ",
        )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Dataframe section ----------
def display_dataframes():
    col1,col2 = st.columns([1,1])
    col3,col4 = st.columns([1,1])

    # ---------- First set of columns ----------
    # First column - Top 5 Occupations
    with col1:
        top_occupations = get_top_occupations()
        st.subheader("Top 5 Occupations")
        st.markdown("Based on the total number of vacancies")
        st.dataframe(top_occupations, use_container_width=True, hide_index=True)

    # Second column - Least Experience Occupations
    with col2:
        st.subheader("Least experience required")
        st.markdown("Occupations that require either no or little experience - not affected by sidebar filter")
        least_experience_occupation_df = get_top_5_least_experience_occupations()
        st.dataframe(least_experience_occupation_df, use_container_width=True, hide_index=True)

    # ---------- Second set of columns ----------
    # Third column - Employers with Highest Avg. Vacancies per Ad
    with col3:
        avg_vacancy_df = average_vacancies_per_job_ad_employer()
        st.subheader("Top Employers by Average Vacancies per Job Ad")
        st.markdown("Ranked by average openings listed per job posting")
        st.dataframe(avg_vacancy_df, use_container_width=True,hide_index=True)

    # Fourth column - Occupations with Most Unique Employers
    with col4:
        st.subheader("Occupations with Highest Number of Unique Employers")
        st.markdown("Top occupations by count of distinct hiring employers")
        top_unique_employer_occupations = get_top_5_occupations_by_unique_employers()
        st.dataframe(top_unique_employer_occupations, use_container_width=True, hide_index=True)


################################################
#   Methods that return values for the KPIs    #
################################################

# Top - Returns the top #1 occupation with the most unique employers hiring
def get_occupation_with_most_unique_employers() -> str:
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()

    query = f"""
        SELECT 
            occupation,
            COUNT(DISTINCT employer_name) AS unique_employer_count
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
            AND (NOW() - INTERVAL '{start_day} day')
            AND experience_required = {requires_experience}
            AND workplace_region IN ({region_string})
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
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

# Column 1 - Returns the number of jobs posted based on current filters
def get_jobs_posted_with_current_filters():
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()
    query = f"""
        SELECT COUNT(*) AS jobs_posted
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL {end_day} DAY)
            AND (NOW() - INTERVAL {start_day} DAY)
            AND experience_required = {requires_experience}
            AND workplace_region IN ({region_string})
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
    """
    df = fetch_data_from_db(query)
    return df['jobs_posted'].values[0]

# Column 2 - Returns the percentage of ads requiring experience
def get_experience_percentage() -> float:
    occupation_field_string, occupation_group_string, _, start_day, end_day, _, region_string = get_sidebar_filters()

    query = f"""
        SELECT 
            ROUND(100.0 * COUNT(*) FILTER (WHERE experience_required = TRUE) / NULLIF(COUNT(*), 0), 2)
            AS percent_with_experience_required
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
            AND (NOW() - INTERVAL '{start_day} day')
            AND workplace_region IN ({region_string})
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
    """
    result = fetch_data_from_db(query)
    return float(result.iloc[0, 0]) if not result.empty and result.iloc[0, 0] is not None else 0.0

# Column 3 - Returns the percentage of ads requiring driver's license
def get_driver_license_percentage() -> float:
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()

    query = f"""
        SELECT 
            ROUND(100.0 * COUNT(*) FILTER (WHERE driver_license = TRUE) / NULLIF(COUNT(*), 0), 2)
            AS percent_with_driver_license_required
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
            AND (NOW() - INTERVAL '{start_day} day')
            AND experience_required = {requires_experience}
            AND workplace_region IN ({region_string})
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
    """
    result = fetch_data_from_db(query)
    return float(result.iloc[0, 0]) if not result.empty and result.iloc[0, 0] is not None else 0.0


################################################
#                  Pie chart                   #
################################################

# Function for getting all occupations for the pie chart
def get_occupational_distribution():
    # Build variables based on the sidebar filters
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()

    query = f"""
            SELECT
                occupation_field,
                occupation_group,
                occupation,
                COUNT(vacancies) AS total_vacancies
            FROM marts.mart_summary
            WHERE occupation_field IN ({occupation_field_string})
                AND occupation_group IN ({occupation_group_string})
                AND experience_required = {requires_experience}
                AND workplace_region IN ({region_string})
                AND publication_date BETWEEN (CURRENT_DATE - INTERVAL '{end_day}' DAY)
                                        AND (CURRENT_DATE - INTERVAL '{start_day}' DAY)
            GROUP BY
                occupation_field,
                occupation_group,
                occupation
            ORDER BY total_vacancies DESC
            """
    data = fetch_data_from_db(query)

    # Check if the data is empty before plotting
    # If the data is not empty, create a pie chart using Plotly
    if not data.empty:
        data["share"] = data["total_vacancies"] / data["total_vacancies"].sum()
        filtered_data = data[data["share"] >= 0.02]

        return filtered_data


################################################
#             Dataframe functions              #
################################################

# Column 1 - Returns the top 5 occupations with the most vacancies
def get_top_occupations() -> pd.DataFrame:
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()

    query = f"""
        SELECT
            occupation AS "Occupation",
            SUM(vacancies) AS "Vacancies"
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
            AND (NOW() - INTERVAL '{start_day} day')
            AND experience_required = {requires_experience}
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
        GROUP BY "Occupation"
        ORDER BY "Vacancies" DESC
        LIMIT 5;
    """
    df = fetch_data_from_db(query)
    return df

# Column 2 - Returns the top 5 occupations with the least experience required
def get_top_5_least_experience_occupations() -> pd.DataFrame:
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()

    query = f"""
        SELECT 
            occupation AS "Occupation",
            SUM(vacancies) AS "Vacancies"
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
            AND (NOW() - INTERVAL '{start_day} day')
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
        GROUP BY "Occupation"
        HAVING ROUND(
            100.0 * COUNT(*) FILTER (WHERE experience_required = TRUE) / NULLIF(COUNT(*), 0),
            2
        ) < 25
        ORDER BY "Vacancies" DESC
        LIMIT 5;
    """
    result = fetch_data_from_db(query)
    return result if not result.empty else pd.DataFrame(columns=["Occupation", "Vacancies"])

# Column 3 - Returns the top 5 employers with the highest average number of openings per ad
def average_vacancies_per_job_ad_employer():
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()

    query = f"""
        SELECT 
            employer_name AS "Employer",
            ROUND(AVG(NULLIF(vacancies, 0)), 2) AS "Average openings",
            COUNT(*) AS "Total ads"
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
            AND (NOW() - INTERVAL '{start_day} day')
            AND experience_required = {requires_experience}
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
            AND "Employer" IS NOT NULL
            AND vacancies BETWEEN 1 AND 50
        GROUP BY "Employer"
        HAVING COUNT(*) >= 3
        ORDER BY "Average openings" DESC
        LIMIT 5;
    """
    df = fetch_data_from_db(query)
    return df

# Column 4 - Returns the top 5 occupations with the most unique employers hiring
def get_top_5_occupations_by_unique_employers() -> pd.DataFrame:
    occupation_field_string, occupation_group_string, _, start_day, end_day, requires_experience, region_string = get_sidebar_filters()

    query = f"""
        SELECT 
            occupation as "Occupation",
            COUNT(DISTINCT employer_name) AS "Employers hiring"
        FROM marts.mart_summary
        WHERE publication_date BETWEEN (NOW() - INTERVAL '{end_day} day')
            AND (NOW() - INTERVAL '{start_day} day')
            AND experience_required = {requires_experience}
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
            AND employer_name IS NOT NULL
        GROUP BY "Occupation"
        ORDER BY "Employers hiring" DESC
        LIMIT 5;
    """

    df = fetch_data_from_db(query)
    return df if not df.empty else pd.DataFrame(columns=["occupation", "unique_employer_count"])


