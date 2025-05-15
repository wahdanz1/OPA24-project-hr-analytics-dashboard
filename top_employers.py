import streamlit as st
from dashboard.utils import fetch_data_from_db, get_sidebar_filters
from dashboard.plots import create_vertical_bar_chart


def top_employers_page():
    st.header("Top Employers per Occupation", divider=True)
    employer_per_occupation()


def employer_per_occupation():
    # Get filters from sidebar
    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    # Main top employers query
    query1 = f"""
        SELECT occupation, 
               employer_name, 
               occupation_field, 
               total_vacancies
        FROM marts.mart_employer_per_occupation
        WHERE occupation_field IN ({name_string})
          AND publication_date BETWEEN (NOW() - INTERVAL {end_day} DAY)
          AND (NOW() - INTERVAL {start_day} DAY)
        GROUP BY occupation, employer_name, occupation_field, total_vacancies
        ORDER BY total_vacancies DESC 
        LIMIT {limit_value}
    """
    st.code(query1, language="sql")
    data1 = fetch_data_from_db(query1)

    if not data1.empty:
        # Main bar chart
        fig1 = create_vertical_bar_chart(
            data1,
            x_value="occupation",
            y_value="total_vacancies",
            y_label="Total vacancies",
            title=f"Top occupation per occupation field",
            color_column="occupation_field",
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        selectbox_key = f"selected_occupation_{name_string}"

        # Ensure available employers
        occupations = data1['occupation'].unique().tolist()

        if (selectbox_key not in st.session_state or not isinstance(st.session_state[selectbox_key], list) or 
            not all(e in occupations for e in st.session_state[selectbox_key]) 
            ):
            # Default to all employers selected if any exist, or empty list
            st.session_state[selectbox_key] = []

        # Multiselect auto binds to the dynamic key (per occupation filter)
        selected_occupations = st.multiselect(
        "Select one or more occupation to explore details",
        occupations,
        default=st.session_state[selectbox_key],
        key=selectbox_key
        )

        # Filter the data
        employer_data = data1[data1['occupation'].isin(selected_occupations)]

        
        with st.expander(f"📊 More insights about selected occupation"):
            total_vacancies = employer_data['total_vacancies'].sum()
            num_employers = employer_data['employer_name'].nunique()

            st.metric("Total Vacancies", int(total_vacancies))
            st.metric("Number of Employers", num_employers)

                # Employers list
            st.write("### Employers Included:")
            employers_list = employer_data['employer_name'].unique().tolist()
            for employer in employers_list:
                st.write(f"- {employer}")

    
            # Use your custom chart function
            fig = create_vertical_bar_chart(
                                            employer_data,
                                            x_value='employer_name',
                                            y_value='total_vacancies',
                                            x_label='Employer',
                                            y_label='Vacancies',
                                            title=f"Vacancies by Occupation for selected employer",
                                            color_column='occupation'
                                             )
    
    st.plotly_chart(fig, use_container_width=True)
    st.divider()