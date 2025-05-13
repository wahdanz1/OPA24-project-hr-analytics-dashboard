import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.utils import fetch_data_from_db, get_sidebar_filters
from dashboard.plots import create_horizontal_bar_chart, create_line_chart


def occupation_trends_page():
    st.header("Occupation Trends Over Time", divider=True)
    everything_test()
    pass

def everything_test():
    
    # Description
    st.markdown("This graph shows the trends in job vacancies over time.")

    requires_experience = "TRUE" if st.checkbox("Requires Experience", value=False) else "FALSE"

    name_string, limit_value, start_day, end_day = get_sidebar_filters()
    # Send a query to the database to get the data for the graph
    bar_query = f"""
            SELECT COUNT(vacancies) AS job_count,occupation FROM marts.mart_occupation_trends_over_time
            WHERE experience_required = {requires_experience}
                AND publication_date
                BETWEEN (NOW() - INTERVAL {end_day} DAY)
                    AND (NOW() - INTERVAL {start_day} DAY)
                AND occupation_field IN ({name_string})
            GROUP BY occupation
            ORDER BY job_count DESC
            LIMIT {limit_value}

        """
    # Query to get job openings over time for top occupations
    line_query = f"""
    WITH ranked_occupations AS (
        SELECT occupation, COUNT(vacancies) AS job_count
        FROM marts.mart_occupation_trends_over_time
        WHERE experience_required = {requires_experience}
            AND occupation_field IN ({name_string})
            AND publication_date BETWEEN (NOW() - INTERVAL {end_day} DAY)
                AND (NOW() - INTERVAL {start_day} DAY)
        GROUP BY occupation
        ORDER BY job_count DESC
        LIMIT {limit_value}
    )

    SELECT
        DATE_TRUNC('day', m.publication_date) AS week,
        m.occupation,
        COUNT(*) AS distinct_occupations
    FROM marts.mart_occupation_trends_over_time m
    JOIN ranked_occupations r ON m.occupation = r.occupation
    WHERE m.experience_required = {requires_experience}
        AND m.publication_date BETWEEN (NOW() - INTERVAL {end_day} DAY)
            AND (NOW() - INTERVAL {start_day} DAY)
    GROUP BY week, m.occupation, r.job_count
    ORDER BY r.job_count DESC, m.occupation, week;

        """


    # Fetch data from the database using the queries
    bar_data = fetch_data_from_db(bar_query)
    line_data = fetch_data_from_db(line_query)




    # Check if the data is empty before plotting   
    if not bar_data.empty:
        # Create a bar chart using Plotly
        bar_fig = create_horizontal_bar_chart(
            data=bar_data,
            x_value="job_count",
            y_value="occupation",
            title="Job openings for selected period",
            x_label="Job Openings",
            y_label="Job Openings",
            color_column="occupation",
            margin=dict(l=50, r=50, t=50, b=40)
        )


        st.plotly_chart(bar_fig, use_container_width=True)

    # Check if the data is empty before plotting    
    if not line_data.empty:
        line_fig = create_line_chart(
            data=line_data,
            x_value="week",
            y_value="distinct_occupations",
            x_label="Date",
            y_label="Job Openings",
            title="Job Openings Over Time",
            color_column="occupation",
        )

        st.plotly_chart(line_fig, use_container_width=True)

