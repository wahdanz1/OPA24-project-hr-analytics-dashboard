import streamlit as st
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart

st.title("HR Dashboard")

# ----- Put your code for the graphs/data below this line! -----

# Header and description for the first graph
st.header("Trends")
st.markdown("")
st.markdown("This graph shows the trends in job vacancies over time.")
st.markdown("")
# Select the number of days to look back
st.markdown("Select the number of days to look back:")
days =st.select_slider(
    "Days",
    options=[ 7, 30, 60, 90, 180],
)
requires_experience = "TRUE" if st.checkbox("Requires Experience", value=False) else "FALSE"

# Send a query to the database to get the data for the graph
query = f"""
        SELECT COUNT(vacancies) AS Jobs,occupation FROM marts.occupation_trends_over_time
        WHERE publication_date >= NOW() - INTERVAL {days} DAY AND experience_required = {requires_experience}
        GROUP BY occupation
        ORDER BY COUNT(vacancies) DESC
        LIMIT 3

    """
data = fetch_data_from_db(query)


# Check if the data is empty before plotting
# If the data is not empty, create a bar chart using Plotly
if not data.empty:
    # Sort by vacancies in descending order
    data = data.sort_values(by="Jobs", ascending=True)

    # Create a bar chart using Plotly
    fig1 = create_horizontal_bar_chart(data=data, x_value="Jobs", y_value="occupation",
                                       title=f"Job Openings in the past {days} days",
                                       x_label="Job Openings",
                                       y_label="Job Openings",
                                       color_collumn="Jobs",
                                       margin=dict(l=50, r=50, t=50, b=40))

    st.plotly_chart(fig1, use_container_width=True)