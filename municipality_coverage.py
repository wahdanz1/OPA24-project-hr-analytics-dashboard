import streamlit as st
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart, create_vertical_bar_chart

def municipality_coverage_page():
    st.header("Muncipality-based data", divider=True)
    distinct_occupations_per_municipality()
    top_3_occupations_per_city()

def distinct_occupations_per_municipality():
    # Description for the first graph
    st.markdown("This graph shows the number of distinct occupations per municipality.")

    # Send a query to the database to get the data for the graph
    limit_value = 5 # Adjust this value as needed
    query1 = f"""
            SELECT *
            FROM marts.mart_distinct_occupations_per_municipality
            LIMIT {limit_value}
        """
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

    # Send a query to the database to get the data for the graph
    query2 = f"""
            SELECT *
            FROM marts.mart_top_occupations_per_city
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

