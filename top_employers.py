import streamlit as st
from dashboard.utils import fetch_data_from_db, get_sidebar_filters, display_dynamic_heading
from dashboard.plots import create_vertical_bar_chart


def top_employers_page():
    display_dynamic_heading()

    top_occupation_per_field()
    st.divider()

def top_occupation_per_field():
    # Get filters from sidebar
    occupation_field_string, occupation_group_string, limit_value, start_day, end_day = get_sidebar_filters()

    # Main top employers query
    query1 = f"""
        WITH filtered_data AS (
            SELECT
                occupation,
                occupation_field,
                SUM(total_vacancies) AS total_vacancies
            FROM marts.mart_top_employers_dynamic
            WHERE occupation_field IN ({occupation_field_string})
            AND occupation_group IN ({occupation_group_string})
            AND publication_date BETWEEN (CURRENT_DATE - INTERVAL '{end_day}' DAY)
                                    AND (CURRENT_DATE - INTERVAL '{start_day}' DAY)
            GROUP BY occupation, occupation_field
        )

        SELECT
            *
        FROM filtered_data
        WHERE total_vacancies IS NOT NULL
        ORDER BY total_vacancies DESC
        LIMIT {limit_value}
    """

    data1 = fetch_data_from_db(query1)

    if not data1.empty:
        # Main bar chart
        fig1 = create_vertical_bar_chart(
            data1,
            x_value="occupation_field",
            x_label="Occupation Field",
            y_value="total_vacancies",
            y_label="Vacancies per Occupation",
            title=" ",
            color_column="occupation",
            hover_data={"total_vacancies": True,
                        "occupation": True,
                        "occupation_field": False},
            text="total_vacancies",
            barmode="group",
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ---------- Top employers per occupation ----------
    # Generate list of available occupations
    occupation_options = data1['occupation'].unique().tolist()
    
    # Occupation selection for the graph
    selected_occupations = st.multiselect(
        "Select one or more occupation to explore details:",
        options=occupation_options,
        key="occupation_selectbox",
    )

    # Get employer data
    employer_query = f"""
        SELECT
            *
        FROM marts.mart_top_employers
    """
    employer_data = fetch_data_from_db(employer_query)
    
    # Filter the employer data based on selected occupation(s)
    filtered_employer_data = employer_data[employer_data['occupation'].isin(selected_occupations)]
    
    # More insights section
    occupation_selection = st.session_state.get("occupation_selectbox")
    if occupation_selection:
        col1, col2, col3 = st.columns(3)

        # Total vacancies
        with col1:
            total_vacancies = filtered_employer_data['total_vacancies'].sum()
            st.metric("Total Vacancies", int(total_vacancies))

        # Number of employers
        with col2:
            num_employers = filtered_employer_data['employer_name'].nunique()
            st.metric("Number of Employers", num_employers)

        # Top 5 employers
        with col3:
            st.write("### Något kul här kanske?")
    
        # Limit by top 10 before plotting to ensure reasonable chart width
        limited_employer_data = filtered_employer_data.head(10)

        # Use your custom chart function
        fig = create_vertical_bar_chart(
            limited_employer_data,
            x_value='employer_name',
            x_label='Employer',
            y_value='total_vacancies',
            y_label='Vacancies',
            title=f"Top employers per region for selected occupation(s)",
            color_column='workplace_region',
            hover_data={"total_vacancies": True,
                        "employer_name": False,
                        "workplace_region": True},
            text="total_vacancies",
        )

        st.plotly_chart(fig, use_container_width=True)
