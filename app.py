import streamlit as st
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
    page_selection = st.radio(
        "Choose a statistics page",
        (
            "Summary", # Page 1
            "Occupation Trends Over Time", # Page 2
            "Municipality Coverage", # Page 3
            "Top Employers", # Page 4
        ),
    )

# Page 1: Occupation Trends Over Time
if page_selection == "Summary":
    # Chipp function calls here
    st.header("Statistics Summary", divider=True)

# Page 2: Occupation Trends Over Time
elif page_selection == "Occupation Trends Over Time":
    import occupation_trends as ot
    ot.occupation_trends_page()

# --------------------------------------------------------
# Page 3: Municipality Coverage
elif page_selection == "Municipality Coverage":
    import municipality_coverage as mc
    mc.municipality_coverage_page()

# --------------------------------------------------------
# Page 4: Top Employers
elif page_selection == "Top Employers":
    import top_employers as te
    st.header("Top Employers per Occupation", divider=True)
    te.top_employers_page()

# --------------------------------------------------------
else:
    st.write("Please select a page from the sidebar.")
