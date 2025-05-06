import streamlit as st
import plotly.express as px
from dashboard.utils import get_distinct_occupations

st.title("HR Dashboard")

# ----- Put your code for the graphs/data below this line! -----

# Header and description for the first graph
st.header("Distinct occupations per municipality")
st.markdown("This graph shows the number of distinct occupations per municipality.")

# Send a query to the database to get the data for the graph
data = get_distinct_occupations()

# Check if the data is empty before plotting
# If the data is not empty, create a bar chart using Plotly
if not data.empty:
    # Sort by distinct_occupations in descending order
    data = data.sort_values(by="distinct_occupations", ascending=True)

    # Create a bar chart using Plotly
    fig = px.bar(
        data,
        x="distinct_occupations",
        y="workplace_municipality",
        orientation="h",
        labels={
            "workplace_municipality": "Municipality",
            "distinct_occupations": "Distinct Occupations"
        },
        title="Distinct Occupations per Municipality",
        color="distinct_occupations",
        color_continuous_scale=px.colors.sequential.Purp,
    )
    st.plotly_chart(fig, use_container_width=True)