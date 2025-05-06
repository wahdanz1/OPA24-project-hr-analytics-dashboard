import streamlit as st
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart, create_line_chart

st.title("HR Dashboard")

# ----- Put your code for the graphs/data below this line! -----

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

# Description for the second area

col1, col2, col3 = st.columns(3)

# Top 3 occupations
with col1:
    st.subheader("Top 3 occupations")
    limit_value = 3 # Adjust this value as needed
    query = f"""
            SELECT *
            FROM marts.occupation_count
            LIMIT {limit_value}
        """
    data = fetch_data_from_db(query)

    # Check if the data is empty before plotting
    # If the data is not empty, create a horizontal bar chart using Plotly
    if not data.empty:
        # Get the top 3 occupations
        for occupation in data["occupation"]:
            st.write(f"• {occupation}")

# Average number of distinct occupations
with col2:
    st.subheader("Average number of distinct occupations")

# Most common occupation
with col3:
    st.subheader("Most common occupation")


# # Send a query to the database to get the data for the graph
# query2 = f"""
#         SELECT *
#         FROM marts.distinct_occupations_per_municipality_over_time
#     """
# data2 = fetch_data_from_db(query2)

# # Check if the data is empty before plotting
# # If the data is not empty, create a line chart using Plotly
# if not data2.empty:
#     fig2 = create_line_chart(data2)
#     st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Description for the third graph
st.markdown("This graph shows the number of distinct occupations per municipality over time.")

# Send a query to the database to get the data for the graph
query3 = f"""
        SELECT *
        FROM marts.distinct_occupations_per_municipality_over_time
    """
data3 = fetch_data_from_db(query3)

# Check if the data is empty before plotting
# If the data is not empty, create a line chart using Plotly
if not data3.empty:
    fig3 = create_line_chart(data3)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()