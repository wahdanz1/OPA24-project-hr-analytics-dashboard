import streamlit as st
from dashboard.utils import get_occupation_field_list, get_occupation_group_list, get_region_list, set_background, build_css_code
# from dashboard.css import css_code

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

with st.sidebar:
    # Sidebar title
    st.title("📊 Job Market Dashboard")

    # ----- Page selection with key -----
    page_selection = st.radio(
        "**Choose something:**",
        (
            "Summary", # Main page
            "Occupation Trends",
            "Geographical Coverage",
            "Top Occupations & Employers",
            "Interactive Assistant"
        ),
        key="page_selection",
    )

    # ----- Occupation field selection with key -----
    occupation_field_choice = st.selectbox(
        "**Occupation field:**",
        options=["All occupation fields"] + get_occupation_field_list(),
        key="occupation_field_choice",
    )
    
    # ----- Occupation group selection with key -----
    occupation_group_choices = st.multiselect(
        "**Occupation group(s):**",
        options=get_occupation_group_list(occupation_field_choice),
        default=[],
        key="occupation_group_choices",
    )

    # ----- Region selection with key -----
    region_choice = st.selectbox(
        "**Region:**",
        options=["All regions"] + get_region_list(
            occupation_field=occupation_field_choice,
            occupation_groups=occupation_group_choices if occupation_group_choices else ["All occupation groups"]
        ),
        key="sidebar_region_choice",
    )

    # # ----- Municipality selection with key -----
    # municipality_choice = st.selectbox(
    #     "**Municipality:**",
    #     options=["All municipalities"] + get_occupation_field_list(),
    #     key="municipality_choice",
    # )

    # ----- Result limit slider with key -----
    # Exclude limit filter from certain pages
    if page_selection != "Summary" and page_selection != "Geographical Coverage":
        limit = st.select_slider(
            label="Results to show:",
            options=[x for x in range(1, 21)],
            value=5,  # Default to the first option
            key="sidebar_limit",
        )

    # ----- Interval range slider with key -----
    start_day, end_day = st.select_slider(
        "Interval (in days):",
        options=[x for x in range(1, 61)],
        value=(1, 60),
        key="sidebar_interval"
    )
    
    # ----- Requires experience-checkbox -----
    requires_experience = st.checkbox(
        "Requires experience?",
        key="sidebar_requires_experience"
    )


    # ----- DBT Documentation-link -----
    st.markdown(
    """
    <a href="https://wahdanz1.github.io/OPA24-project-hr-analytics-dashboard/" target="_blank">
        <button class="dbt-button">📘 View DBT Documentation</button>
    </a>
    """,
    unsafe_allow_html=True
    )

built_css_code = build_css_code(page_selection)
# Retrieve css code and inject it into the dashboard html
st.markdown(
    built_css_code,
    unsafe_allow_html=True,
)

################################################
#              Page if-statement               #
################################################

# Page 1: Occupation Trends Over Time
if page_selection == "Summary":
    set_background(page_selection)
    import dashboard.summary as sm
    sm.summary_page()

# --------------------------------------------------------
# Page 2: Occupation Trends Over Time
elif page_selection == "Occupation Trends":
    set_background(page_selection)
    import dashboard.occupation_trends as ot
    ot.occupation_trends_page()

# --------------------------------------------------------
# Page 3: Geographical Coverage
elif page_selection == "Geographical Coverage":
    set_background(page_selection)
    import dashboard.geo_coverage as gc
    gc.geographical_coverage_page()

# --------------------------------------------------------
# Page 4: Top Employers
elif page_selection == "Top Occupations & Employers":
    set_background(page_selection)
    import dashboard.top_employers as te
    te.top_employers_page()

# --------------------------------------------------------
# Page 5: Interactive Assistant
elif page_selection == "Interactive Assistant":
    from ai.chat import open_chat
    open_chat()
# --------------------------------------------------------
else:
    st.write("Please select a page from the sidebar.")
