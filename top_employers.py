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
            x_value="employer_name",
            y_value="total_vacancies",
            y_label="Total vacancies",
            title=f"Top employer per {name_string}",
            color_column="occupation",
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        selectbox_key = f"selected_employer_{name_string}"

        # Ensure available employers
        employers = data1['employer_name'].unique().tolist()

        # Initialize state if invalid or missing
        if selectbox_key not in st.session_state or st.session_state[selectbox_key] not in employers:
            st.session_state[selectbox_key] = employers[0] if employers else None

        # Selectbox auto binds to the dynamic key (per occupation filter)
        selected_employer = st.selectbox(
            "Select an employer to explore details",
            employers,
            index=employers.index(st.session_state[selectbox_key]),
            key=selectbox_key
        )

        # Filter the data
        employer_data = data1[data1['employer_name'] == selected_employer]

        with st.expander(f"📊 More insights about {selected_employer}"):
            st.metric("Total Vacancies", int(employer_data['total_vacancies'].sum()))
            st.bar_chart(employer_data.set_index('occupation')['total_vacancies'])

    else:
        st.warning("No data found for the selected filters.")
