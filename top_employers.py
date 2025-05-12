import streamlit as st 
from dashboard.utils import fetch_data_from_db, get_sidebar_filters
from dashboard.plots import create_vertical_bar_chart

def top_employers_page():
    st.header("Top Employers per Occupation", divider=True)
    employer_per_occupation()


def employer_per_occupation():

    name_string, limit_value, start_day, end_day = get_sidebar_filters()

    query1 = f"""
            SELECT occupation, 
            employer_name, 
            occupation_field, 
            total_vacancies,
            FROM marts.mart_employer_per_occupation
            WHERE occupation_field IN ({name_string})
            -- GROUP BY occupation, employer_name, occupation_field, total_vacancies
            ORDER BY total_vacancies DESC 
            LIMIT {limit_value}
                """
    st.code(query1,language="sql")
    data1 = fetch_data_from_db(query1)


    if not data1.empty:
       # data1 = data1.sort_values(by="ads_posted", ascending=False)
        
        fig1 = create_vertical_bar_chart(data1,
            x_value = "employer_name",
            y_value = "total_vacancies",
            y_label = "Total vacancies",
            title="Top employer per occupation",
            color_column="total_vacancies",
            )
        st.plotly_chart(fig1, use_container_width=True)

    st.divider()

