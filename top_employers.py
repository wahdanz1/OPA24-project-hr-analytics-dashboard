import streamlit as st 
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_vertical_bar_chart, create_line_chart

def top_employers_page():
    st.header("Top Employers per Occupation", divider=True)
    employer_per_occupation()
    top_per_selected_occupation()


def employer_per_occupation():

    query1 = f"""SELECT * FROM marts.mart_employer_per_occupation"""
    st.code(query1,language="sql")
    data1 = fetch_data_from_db(query1)


    if not data1.empty:
        data1 = data1.sort_values(by="ads_posted_last_30_days", ascending=False).head(10)
        
        fig1 = create_vertical_bar_chart(data1,
            x_value = "employer_name",
            y_value = "ads_posted_last_30_days",
            title="Top employer per occupation",
            color_column="ads_posted_last_30_days",
            )
        st.plotly_chart(fig1, use_container_width=True)

    st.divider()

def top_per_selected_occupation():

    query2 = f"""SELECT * FROM marts.mart_employer_per_occupation"""
    st.code(query2,language="sql")
    data2 = fetch_data_from_db(query2)
    
    unique_occupation = sorted(data2["occupation"].dropna().unique())

    selected_occupation = st.multiselect(
        "Select one or more ",
        options=unique_occupation,
    )

    
    filtered_data2 = data2[data2["occupation"].isin(selected_occupation)]

    if not filtered_data2.empty:     
        fig1 = create_vertical_bar_chart(filtered_data2,
            x_value = "employer_name",
            y_value = "ads_posted_last_30_days",
            title="Distinct Occupations per Municipality",
            color_column="ads_posted_last_30_days",
            )
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = create_line_chart(filtered_data2,
            x_value = "employer_name",
            y_value = "ads_posted_last_30_days",
            title= "occupations over time",
            color_column= "occupation",
            )
        st.plotly_chart(fig2,use_container_width= True)

    st.divider()
