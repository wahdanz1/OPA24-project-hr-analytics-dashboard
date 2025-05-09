import streamlit as st
from dashboard.utils import fetch_data_from_db, get_sidebar_filters
from dashboard.plots import create_horizontal_bar_chart

def municipality_coverage_page():
    st.header("Municipality Coverage", divider=True)
    st.markdown("This page provides insights into the coverage of job ads across different municipalities.")
    distinct_occupations_per_municipality()

def distinct_occupations_per_municipality():
    # Description for the first graph
    st.markdown("This graph shows the number of distinct occupations per municipality.")

    # Build the string for the SQL query based on the selected occupation field
    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    # Send a query to the database to get the data for the graph
    query1 = f"""
            SELECT *
            FROM marts.mart_distinct_occupations_per_municipality
            WHERE occupation_field IN ({name_string})
            AND publication_date
                BETWEEN (NOW() - INTERVAL {end_day} DAY)
                    AND (NOW() - INTERVAL {start_day} DAY)
            LIMIT {limit_value}
            """
    st.code(query1, language="sql")
    data1 = fetch_data_from_db(query1)

    # Check if the data is empty before plotting
    # If the data is not empty, create a horizontal bar chart using Plotly
    if not data1.empty:
        # Sort by distinct_occupations in descending order
        data1 = data1.sort_values(by="distinct_occupations", ascending=True)

        fig1 = create_horizontal_bar_chart(
            data1,
            x_value="distinct_occupations",
            y_value="workplace_municipality",
            y_label="Distinct Occupations per Municipality",
            title="Distinct Occupations per Municipality",
            color_column="distinct_occupations",
            hover_template="%{y} has %{x} distinct occupations"
            )
        st.plotly_chart(fig1, use_container_width=True)

    st.divider()