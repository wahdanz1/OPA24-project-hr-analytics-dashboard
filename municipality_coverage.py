import streamlit as st
from dashboard.utils import fetch_data_from_db, set_occupation_field_name
from dashboard.plots import create_horizontal_bar_chart, create_vertical_bar_chart

def municipality_coverage_page():
    st.header("Municipality Coverage", divider=True)
    st.markdown("This page provides insights into the coverage of job ads across different municipalities.")
    distinct_occupations_per_municipality()
    top_3_occupations_per_city()

def distinct_occupations_per_municipality():
    # Description for the first graph
    st.markdown("This graph shows the number of distinct occupations per municipality.")

    # Check if the occupation_field is "All fields" and set it to None if so
    occupation_field_choice = st.session_state.get("occupation_field_choice", ["All fields"])
    occupation_field_names = set_occupation_field_name(occupation_field_choice)

    # Based on the occupation_field_id, set the WHERE clause for the SQL query
    if occupation_field_names is None:
        where_clause = ""
    else:
        # Create a list of quoted strings for SQL IN clause
        id_list = ", ".join(f"'{id}'" for id in occupation_field_names)
        where_clause = f"WHERE occupation_field IN ({id_list})"

    # Send a query to the database to get the data for the graph
    limit_value = 15 # Adjust this value as needed
    query1 = f"""
            SELECT
                workplace_municipality,
                distinct_occupations,
            FROM marts.mart_distinct_occupations_per_municipality
            {where_clause}
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

def top_3_occupations_per_city():
    # Description for the first graph
    st.markdown("This graph shows the top 3 occupations per city. You can filter the data by municipality.")

    # Check if the occupation_field is "All fields" and set it to None if so
    occupation_field_choice = st.session_state.get("occupation_field_choice", ["All fields"])
    occupation_field_names = set_occupation_field_name(occupation_field_choice)

    # Based on the occupation_field_id, set the WHERE clause for the SQL query
    if occupation_field_names is None:
        where_clause = ""
    else:
        # Create a list of quoted strings for SQL IN clause
        id_list = ", ".join(f"'{id}'" for id in occupation_field_names)
        where_clause = f"WHERE occupation_field IN ({id_list})"

    # Send a query to the database to get the data for the graph
    query2 = f"""
            SELECT *
            FROM marts.mart_top_occupations_per_city
            {where_clause}
        """
    data2 = fetch_data_from_db(query2)

    unique_municipalities = sorted(data2["workplace_municipality"].dropna().unique())

    selected_municipalities = st.multiselect(
        "Select one or more municipalities",
        options=unique_municipalities,
        default='Göteborg',  # Default to the first municipality
    )

    filtered_data2 = data2[data2["workplace_municipality"].isin(selected_municipalities)]

    # Check if the data is empty before plotting
    # If the data is not empty, create a horizontal bar chart using Plotly
    if not filtered_data2.empty:
        fig2 = create_vertical_bar_chart(
            filtered_data2,
            x_value="workplace_city",
            y_value="job_ad_count",
            x_label="City",
            y_label="Number of job ads",
            title="Top 3 Occupations per City",
            color_column="occupation",
            )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No data available for the selected municipality.")

    st.divider()

