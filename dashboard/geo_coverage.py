import streamlit as st
from .utils import fetch_data_from_db, get_sidebar_filters, get_occupation_field_list
from .plots import create_vertical_bar_chart, create_marimekko_chart

def geographical_coverage_page():
    st.header("🌍 Geographical Coverage", divider=True)
    st.markdown("This page provides insights into the coverage of job ads across different municipalities.")
    # top_occupations_per_municipality()
    # st.divider()
    top_occupation_groups_marimekko()

# Function for creating and displaying marimekko chart on page
def top_occupation_groups_marimekko(top_n: int = 10):
    st.markdown("This Marimekko chart shows the top occupation groups per municipality based on total vacancies.")

    # Sidebar filters
    occupation_field_choice = st.session_state.get("occupation_field_choice", "All occupation fields")
    _, occupation_group_string, _, start_day, end_day, _, region_string = get_sidebar_filters()

    # Determine selected occupation fields
    occupation_fields = (
        get_occupation_field_list() if occupation_field_choice == "All occupation fields"
        else [occupation_field_choice]
    )

    # Emoji for field headers
    FIELD_EMOJIS = {
        "Administration, ekonomi, juridik": "💼",
        "Försäljning, inköp, marknadsföring": "💹",
        "Hälso- och sjukvård": "🏥",
    }

    with st.spinner("Loading charts..."):
        for occupation_field in occupation_fields:
            emoji = FIELD_EMOJIS.get(occupation_field, "")
            if occupation_field_choice == "All occupation fields":
                st.subheader(f"{emoji} {occupation_field}")

            # SQL Query
            query = f"""
                WITH filtered_data AS (
                    SELECT
                        workplace_municipality,
                        occupation_group,
                        occupation_field,
                        workplace_region,
                        SUM(total_vacancies) AS total_vacancies
                    FROM marts.mart_occupation_group_vacancy_totals
                    WHERE occupation_field = '{occupation_field}'
                        AND workplace_region IN ({region_string})
                        AND publication_date BETWEEN (CURRENT_DATE - INTERVAL '{end_day}' DAY)
                                                AND (CURRENT_DATE - INTERVAL '{start_day}' DAY)
                    GROUP BY workplace_municipality, occupation_group, occupation_field, workplace_region
                )
                SELECT *,
                    ROW_NUMBER() OVER (
                        PARTITION BY workplace_municipality, occupation_field
                        ORDER BY total_vacancies DESC
                    ) AS rank
                FROM filtered_data
                WHERE total_vacancies IS NOT NULL
                QUALIFY rank <= 3
                ORDER BY total_vacancies DESC
            """
            data = fetch_data_from_db(query)

            if data.empty:
                st.info(f"No data found for {occupation_field}.")
                continue

            # Prepare top municipalities and calculate Marimekko geometry
            top_munis = (
                data.groupby("workplace_municipality")["total_vacancies"]
                .sum()
                .reset_index()
                .sort_values("total_vacancies", ascending=False)
                .head(top_n)
            )

            top_munis["width"] = top_munis["total_vacancies"] / top_munis["total_vacancies"].sum()
            top_munis["x_base"] = top_munis["width"].cumsum() - top_munis["width"]
            top_munis["x_center"] = top_munis["x_base"] + top_munis["width"] / 2

            # Filter + merge back x/width data
            data = data[data["workplace_municipality"].isin(top_munis["workplace_municipality"])]
            data = data.merge(
                top_munis[["workplace_municipality", "x_base", "x_center", "width"]],
                on="workplace_municipality"
            )

            # Calculate relative height (i.e. share of municipality)
            data["y_total"] = data.groupby("workplace_municipality")["total_vacancies"].transform("sum")
            data["height"] = data["total_vacancies"] / data["y_total"]

            # Plot it!
            fig = create_marimekko_chart(
                data=data,
                municipality_labels=top_munis[["workplace_municipality", "x_center", "width", "x_base"]],
            )
            st.plotly_chart(fig, use_container_width=True)

            st.divider()

# Function for creating and displaying horizontal bar chart on page
def top_occupations_per_municipality():
    # Description for the graph
    st.markdown("This graph shows the top occupations per municipality based on total vacancies.")

    # Build variables based on the sidebar filters
    occupation_field_string, _, _, start_day, end_day, _, region_string = get_sidebar_filters()

    # Send a query to the database to get the data for the graph
    query1 = f"""
        WITH filtered_data AS (
            SELECT
                workplace_municipality,
                occupation,
                occupation_field,
                workplace_region,
                SUM(total_vacancies) AS total_vacancies
            FROM marts.mart_occupation_group_vacancy_totals
            WHERE occupation_field IN ({occupation_field_string})
                AND workplace_region IN ({region_string})
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
        data1 = data1.head(20)
        fig1 = create_vertical_bar_chart(
            data1,
            x_value="workplace_municipality",
            x_label="Municipality",
            y_value="rank_score",
            y_label="Vacancies per Occupation",
            title=f"Top Occupations per Municipality",
            color_column="occupation",
            hover_data={"total_vacancies": True,
                        "rank_score": False,
                        "workplace_municipality": False},
            showticklabels=False,
            text="total_vacancies",
            )
        st.plotly_chart(fig1, use_container_width=True)

        with st.expander("SQL Query", expanded=False):
            st.markdown("This is the SQL code used to generate the graph:")
            st.code(query1, language="sql")