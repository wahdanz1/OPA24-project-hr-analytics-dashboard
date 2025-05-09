import streamlit as st

from dashboard.sidebar_stats import sidebar_stats
sidebar = sidebar_stats()
st.set_page_config(layout="wide")

st.title("HR Dashboard")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    # Sidebar title
    st.title("HR Dashboard")

    # Page selection with key
    page_selection = st.radio(
        "Choose something:",
        (
            "Summary", # Main page
            "Occupation Trends",
            "Municipality Coverage",
            "Top Employers",
        ),
        key="page_selection",
    )

    ## Occupation field selection with key
    occupation_field_choice = st.multiselect(
        "Select one or more occupation fields",
        options=[
            "Administration, finance & law",
            "Sales & marketing",
            "Healthcare",
        ],
        # default=[],
        key="occupation_field_choice",
    )
    # Select how many top results to show
    st.markdown("Select how many top results to show:")
    limit = st.select_slider(
        "Top N",
        options=[x for x in range(1, 21)],
        value=5,  # Default to the first option
    )
    sidebar.set_limit(limit)
    # Select how many days to look back
    st.markdown("Select the number of days to look back:")
    days = st.select_slider(
        "Days",
        options=[x for x in range(1, 181)],
        value=30,  # Default to the first option
    )
    sidebar.set_days(days)


# Page 1: Occupation Trends Over Time
if page_selection == "Summary":
    # Chipp function calls here
    st.header("Summary", divider=True)

# Page 2: Occupation Trends Over Time
elif page_selection == "Occupation Trends":
    import occupation_trends as ot
    ot.occupation_trends_page(sidebar)

# --------------------------------------------------------
# Page 3: Municipality Coverage
elif page_selection == "Municipality Coverage":
    import municipality_coverage as mc
    mc.municipality_coverage_page()

# --------------------------------------------------------
# Page 4: Top Employers
elif page_selection == "Top Employers":
    import top_employers as te
    te.top_employers_page()

# --------------------------------------------------------
else:
    st.write("Please select a page from the sidebar.")
