import streamlit as st
from .utils import fetch_data_from_db, get_sidebar_filters, display_dynamic_heading, wrap_label
from .plots import create_horizontal_bar_chart, create_line_chart

def occupation_trends_page():
    display_dynamic_heading()
    
    # Description
    st.markdown("This graph shows the trends in job openings over time, based on the interval set in the sidebar.")

    bar_plot()
    st.divider()
    line_plot()

# Bar chart area
def bar_plot():
    occupation_field_string, occupation_group_string, limit_value, start_day, end_day, requires_experience, region_string = get_sidebar_filters()
    # Send a query to the database to get the data for the graph
    bar_query = f"""
            SELECT
                COUNT(vacancies) AS job_count,
                occupation
            FROM marts.mart_occupation_trends_over_time
            WHERE experience_required = {requires_experience}
                AND publication_date
                BETWEEN (NOW() - INTERVAL {end_day} DAY)
                    AND (NOW() - INTERVAL {start_day} DAY)
                AND occupation_field IN ({occupation_field_string})
                AND occupation_group IN ({occupation_group_string})
            GROUP BY occupation
            ORDER BY job_count DESC
            LIMIT {limit_value}
        """

    # Fetch data from the database using the queries
    bar_data = fetch_data_from_db(bar_query)

    # Check if the data is empty before plotting   
    if not bar_data.empty:
        # Create a bar chart using Plotly
        bar_fig = create_horizontal_bar_chart(
            data=bar_data,
            x_value="job_count",
            y_value="occupation",
            title="Job openings for selected period",
            x_label="Job Openings",
            y_label="Occupation",
            color_column="occupation",
            margin=dict(l=50, r=50, t=50, b=40),
            text="job_count",
        )

        st.plotly_chart(bar_fig, use_container_width=True)

# Line chart area
def line_plot():
    # Get sidebar filters
    occupation_field_string, occupation_group_string, limit_value, start_day, end_day, requires_experience, region_string = get_sidebar_filters()
    
    # Query to get job openings over time for top occupations
    line_query = f"""
    WITH ranked_occupations AS (
        SELECT
            occupation,
            COUNT(vacancies) AS job_count
        FROM marts.mart_occupation_trends_over_time
        WHERE experience_required = {requires_experience}
            AND occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
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

    # Fetch data from the database using the query
    line_data = fetch_data_from_db(line_query)

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
