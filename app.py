import streamlit as st
from dashboard.utils import get_occupation_field_list, get_occupation_group_list, set_background

st.set_page_config(page_title="HR Dashboard", layout="wide")

# Old CSS styling for sidebar
        # section[data-testid="stSidebar"] {
        #     width: 350px !important;
        #     background-color: rgb(38, 39, 48);
        # }

# CSS to set the sidebar width
st.markdown(
    """
    <style>
        /* Styling for all containers inside the main section */
        div.stMainBlockContainer div[data-testid="stVerticalBlock"] {
            background: rgb(38, 39, 48);
            padding: 2rem !important;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* Header styling */
        header.stAppHeader {
            background: transparent !important;
        }

        /* Target all element containers */
        div[data-testid="stElementContainer"][width] {
            width: auto !important;
            max-width: 100% !important;
        }

        /* Optional: make tables and charts inside behave responsively too */
        div[data-testid="stElementContainer"] > div {
            max-width: 100% !important;
        }
        
        /* Heading (h3) styling */
        div[data-testid="stHeadingWithActionElements"] h3 {
            color: rgb(197, 44, 95) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    # Sidebar title
    st.title("📊 HR Dashboard")

    # Page selection with key
    page_selection = st.radio(
        "**Choose something:**",
        (
            "Summary", # Main page
            "Occupation Trends",
            "Geographical Coverage",
            "Top Occupations & Employers",
        ),
        key="page_selection",
    )

    ## Occupation field selection with key
    occupation_field_choice = st.selectbox(
        "**Occupation field:**",
        options=["All occupation fields"] + get_occupation_field_list(),
        key="occupation_field_choice",
    )

    ## Occupation group selection with key
    occupation_group_choices = st.multiselect(
        "**Occupation group(s):**",
        options=get_occupation_group_list(occupation_field_choice),
        key="occupation_group_choices",
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
    set_background(page_selection)
    import summary as sm
    sm.summary_page()

# --------------------------------------------------------
# Page 2: Occupation Trends Over Time
elif page_selection == "Occupation Trends":
    set_background(page_selection)
    import occupation_trends as ot
    ot.occupation_trends_page()

# --------------------------------------------------------
# Page 3: Geographical Coverage
elif page_selection == "Geographical Coverage":
    set_background(page_selection)
    import geo_coverage as gc
    gc.geographical_coverage_page()

# --------------------------------------------------------
# Page 4: Top Employers
elif page_selection == "Top Occupations & Employers":
    set_background(page_selection)
    import top_employers as te
    te.top_employers_page()

# --------------------------------------------------------
else:
    st.write("Please select a page from the sidebar.")
