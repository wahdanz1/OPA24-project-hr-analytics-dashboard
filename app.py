import streamlit as st
st.set_page_config(layout="wide")

import occupation_trends as ot
import municipality_coverage as mc
import top_employers as te

st.title("HR Dashboard")

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
    ot.occupation_trends_page()

# --------------------------------------------------------
# Page 3: Municipality Coverage
elif page_selection == "Municipality Coverage":
    mc.municipality_coverage_page()

# --------------------------------------------------------
# Page 4: Top Employers
elif page_selection == "Top Employers":
    st.header("Top Employers per Occupation", divider=True)
    te.top_employers_page()

# --------------------------------------------------------
else:
    st.write("Please select a page from the sidebar.")
