import streamlit as st
import pandas as pd
from dashboard.utils import fetch_data_from_db, get_sidebar_filters
from dashboard.plots import create_horizontal_bar_chart, create_vertical_bar_chart

def municipality_coverage_page():
    st.header("Municipality Coverage", divider=True)
    st.markdown("This page provides insights into the coverage of job ads across different municipalities.")
    top_occupations_per_municipality()
    # st.divider()

def top_occupations_per_municipality():
    # Description for the graph
    st.markdown("This graph shows the top occupations per municipality based on total vacancies.")

    # Build the string for the SQL query based on the selected occupation field
    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    region_query = """
                    SELECT DISTINCT workplace_region
                    FROM marts.mart_top_occupations_dynamic
                    WHERE workplace_region IS NOT NULL
                    ORDER BY workplace_region
                    """
    regions = fetch_data_from_db(region_query)
    region_options = regions["workplace_region"].tolist()
    
    # Region selection for the graph
    selected_region = st.selectbox(
        "Select a region",
        options=region_options,
        index=0,
        key="region_selectbox"
    )

    # Send a query to the database to get the data for the graph
    query1 = f"""
        WITH filtered_data AS (
            SELECT
                workplace_municipality,
                occupation,
                occupation_field,
                workplace_region,
                SUM(total_vacancies) AS total_vacancies
            FROM marts.mart_top_occupations_dynamic
            WHERE occupation_field IN ({name_string})
            AND workplace_region = '{selected_region}'
            AND publication_date BETWEEN (CURRENT_DATE - INTERVAL '{end_day}' DAY)
                                    AND (CURRENT_DATE - INTERVAL '{start_day}' DAY)
            GROUP BY workplace_municipality, occupation, occupation_field, workplace_region
        )

        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY workplace_municipality, occupation_field
                ORDER BY total_vacancies DESC
            ) AS rank
        FROM filtered_data
        WHERE total_vacancies IS NOT NULL
        QUALIFY rank <= 3
        ORDER BY total_vacancies DESC
    """
    data1 = fetch_data_from_db(query1)

    # Check if the data is empty before plotting
    # If the data is not empty, create a vertical bar chart using Plotly
    if not data1.empty:
        # Add if-statement for whether data1 contains a lot of rows, meaning the
        # selected region has a lot of municipalities which would cause the chart
        # to be too wide

        # Reverse order for the rank to have rank 1 be the tallest bar
        data1["rank_score"] = 4 - data1["rank"]  # If rank is 1, score is 3; rank 2 → 2; rank 3 → 1

        fig1 = create_vertical_bar_chart(
            data1,
            x_value="workplace_municipality",
            x_label="Municipality",
            y_value="rank_score",
            y_label="Vacancies per Occupation",
            title=f"Top Occupations per Municipality (in {selected_region})",
            color_column="occupation",
            hover_data={"total_vacancies": True,
                        "rank_score": False,
                        "workplace_municipality": False},
            text="total_vacancies",
            showticklabels=False,
            )
        st.plotly_chart(fig1, use_container_width=True)

        with st.expander("SQL Query", expanded=False):
            st.markdown("This is the SQL code used to generate the graph:")
            st.code(query1, language="sql")