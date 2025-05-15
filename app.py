import streamlit as st

st.set_page_config(page_title="HR Dashboard", layout="wide")

# CSS to set the sidebar width
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 350px !important;
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
            "Geographical Coverage",
            "Top Occupations & Employers",
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

    if page_selection != "Summary" and page_selection != "Geographical Coverage":
        # Result limit slider with key
        limit = st.select_slider(
            label="Results to show:",
            options=[x for x in range(1, 21)],
            value=5,  # Default to the first option
            key="sidebar_limit",
        )

    # Interval range slider with key
    start_day, end_day = st.select_slider(
        "Interval (in days):",
        options=[x for x in range(1, 61)],
        value=(1, 60),
        key="sidebar_interval"
    )

# Page 1: Occupation Trends Over Time
if page_selection == "Summary":
    import summary as sm
    sm.summary_page()
    

# --------------------------------------------------------
# Page 2: Occupation Trends Over Time
elif page_selection == "Occupation Trends":
    import occupation_trends as ot
    ot.occupation_trends_page()

# --------------------------------------------------------
# Page 3: Geographical Coverage
elif page_selection == "Geographical Coverage":
    import geographical_coverage as gc
    gc.geographical_coverage_page()

# --------------------------------------------------------
# Page 4: Top Employers
elif page_selection == "Top Occupations & Employers":
    import top_employers as te
    te.top_employers_page()

# --------------------------------------------------------
else:
    st.write("Please select a page from the sidebar.")
