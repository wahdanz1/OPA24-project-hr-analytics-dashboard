import streamlit as st
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart

st.title("HR Dashboard")

# ----- Put your code for the graphs/data below this line! -----

# Header and description for the first graph
st.header("Muncipality-based data")
st.markdown("This graph shows the number of distinct occupations per municipality.")

# Send a query to the database to get the data for the graph
query = f"""
        SELECT *
        FROM marts.distinct_occupations_per_municipality
        LIMIT 5
    """
data = fetch_data_from_db(query)

# Check if the data is empty before plotting
# If the data is not empty, create a bar chart using Plotly
if not data.empty:
    # Sort by distinct_occupations in descending order
    data = data.sort_values(by="distinct_occupations", ascending=True)

    # Create a bar chart using Plotly
    fig1 = create_horizontal_bar_chart(data)
    st.plotly_chart(fig1, use_container_width=True)