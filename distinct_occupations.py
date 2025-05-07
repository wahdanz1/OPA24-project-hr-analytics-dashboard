import streamlit as st
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart, create_line_chart

st.title("HR Dashboard")

# Header and description for the first graph
st.header("Muncipality-based data", divider=True)

# Description for the first graph
st.markdown("This graph shows the number of distinct occupations per municipality.")

# Send a query to the database to get the data for the graph
limit_value = 5 # Adjust this value as needed
query1 = f"""
        SELECT *
        FROM marts.distinct_occupations_per_municipality
        LIMIT {limit_value}
    """
data1 = fetch_data_from_db(query1)

# Check if the data is empty before plotting
# If the data is not empty, create a horizontal bar chart using Plotly
if not data1.empty:
    # Sort by distinct_occupations in descending order
    data1 = data1.sort_values(by="distinct_occupations", ascending=True)

    fig1 = create_horizontal_bar_chart(data1)
    st.plotly_chart(fig1, use_container_width=True)

st.divider()

# Header and description for the first graph
st.header("Muncipality-based data", divider=True)

# Description for the first graph
st.markdown("This graph shows the top 3 occupations per city. You can filter the data by municipality.")

# Create a selectbox for the user to choose a municipality
municipality = st.selectbox(
    "Select a municipality",
    options=data1["municipality"].unique(),
    index=0  # Default to the first municipality
)

# Send a query to the database to get the data for the graph
query1 = f"""
        SELECT *
        FROM marts.distinct_occupations_per_municipality
    """
data2 = fetch_data_from_db(query1)

# Check if the data is empty before plotting
# If the data is not empty, create a horizontal bar chart using Plotly
if not data2.empty:
    fig2 = create_horizontal_bar_chart(data2)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

