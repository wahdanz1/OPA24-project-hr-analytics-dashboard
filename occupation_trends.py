import streamlit as st
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart, create_line_chart

def occupation_trends_page():
    st.header("Occupation Trends Over Time", divider=True)
    pass

# Description
st.markdown("This graph shows the trends in job vacancies over time.")
# Select the number of days to look back
st.markdown("Select the number of days to look back:")

days =st.select_slider(
    "Days",
    options=[x for x in range(1, 180)],
)
limit = st.select_slider(
    "How many occupations to show?",
    options=[x for x in range(1, 21)],
)
requires_experience = "TRUE" if st.checkbox("Requires Experience", value=False) else "FALSE"

# Send a query to the database to get the data for the graph
bar_query = f"""
        SELECT COUNT(vacancies) AS Jobs,occupation FROM marts.occupation_trends_over_time
        WHERE publication_date >= NOW() - INTERVAL {days} DAY AND experience_required = {requires_experience}
        GROUP BY occupation
        ORDER BY COUNT(vacancies) DESC
        LIMIT {limit}

    """
# Query to get job openings over time for top occupations
line_query = f"""
    WITH top_occupations AS (
        SELECT occupation
        FROM marts.occupation_trends_over_time
        WHERE publication_date >= NOW() - INTERVAL {days} DAY
            AND experience_required = {requires_experience}
        GROUP BY occupation
        ORDER BY COUNT(*) DESC
        LIMIT {limit}
    )
    SELECT
        DATE_TRUNC('day', publication_date) AS week,
        occupation,
        COUNT(*) AS distinct_occupations
    FROM marts.occupation_trends_over_time
    WHERE publication_date >= NOW() - INTERVAL {days} DAY
        AND experience_required = {requires_experience}
        AND occupation IN (SELECT occupation FROM top_occupations)
    GROUP BY week, occupation
    ORDER BY week, occupation;
"""
# Fetch data from the database using the queries
bar_data = fetch_data_from_db(bar_query)
line_data = fetch_data_from_db(line_query)

# Check if the data is empty before plotting
# If the data is not empty, create a bar chart using Plotly

    



# Create two columns for the bar and line charts
col1, col2 = st.columns([1,2])


with col1:
    # Check if the data is empty before plotting   
    if not bar_data.empty:
        # Sort by vacancies in descending order
        bar_data = bar_data.sort_values(by="Jobs", ascending=True)
        # Create a bar chart using Plotly
        bar_fig = create_horizontal_bar_chart(data=bar_data, x_value="Jobs", y_value="occupation",
                                        title=f"Job Openings in the past {days} days",
                                        x_label="Job Openings",
                                        y_label="Job Openings",
                                        color_column="Jobs",
                                        margin=dict(l=50, r=50, t=50, b=40))

        st.plotly_chart(bar_fig, use_container_width=True)
# If the data is not empty, create a line chart using Plotly
with col2:
    # Check if the data is empty before plotting    
    if not line_data.empty:
        line_fig = create_line_chart(
            data=line_data,
            x_value="week",
            y_value="distinct_occupations",
            x_label="Date",
            y_label="Job Openings",
            title=f"Job Openings Over Time (Past {days} Days)",
            color_column="occupation"
        )
        st.plotly_chart(line_fig, use_container_width=True)

