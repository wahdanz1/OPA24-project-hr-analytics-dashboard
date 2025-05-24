import pandas as pd
import streamlit as st
from pipeline.db import DuckDBConnection
from config import db_path
import base64

# Function for fetching data from the database
def fetch_data_from_db(query: str, params=None) -> pd.DataFrame:
    with DuckDBConnection(db_path) as conn:
        return conn.query(query, params)

# Function for getting the sidebar filters from the session state
def get_sidebar_filters():
    # Get occupation field choice from session
    occupation_field_choice = st.session_state.get("occupation_field_choice", "All occupation fields")

    # If "All", fetch all fields from DB, else just use the selected one
    if occupation_field_choice == "All occupation fields":
        occupation_fields = get_occupation_field_list()
    else:
        occupation_fields = [occupation_field_choice]

    occupation_field_string = ", ".join(f"'{name}'" for name in occupation_fields)

    # Occupation groups (same logic)
    occupation_group_choices = st.session_state.get("occupation_group_choices", [])
    if occupation_group_choices:
        occupation_group_string = ", ".join(f"'{group}'" for group in occupation_group_choices)
    else:
        all_groups = get_occupation_group_list()
        occupation_group_string = ", ".join(f"'{group}'" for group in all_groups)

    # Get limit and interval values
    limit_value = st.session_state.get("sidebar_limit")
    interval_value = st.session_state.get("sidebar_interval")
    start_day, end_day = sorted(interval_value)

    return occupation_field_string, occupation_group_string, limit_value, start_day, end_day

# Function to get the list of occupation fields from the database
# Returns a list of unique occupation fields to be used in the sidebar
st.cache_data
def get_occupation_field_list():
    query = f"""
        SELECT DISTINCT occupation_field
        FROM marts.mart_summary
        WHERE occupation_field IS NOT NULL
        ORDER BY occupation_field;
    """
    df = fetch_data_from_db(query)
    return df["occupation_field"].tolist() if not df.empty else []

# Function to get the list of occupation groups from the database
# Returns a list of unique occupation groups to be used in the sidebar
def get_occupation_group_list(occupation_field: str = "All occupation fields") -> list:
    if occupation_field == "All occupation fields":
        query = """
            SELECT DISTINCT occupation_group
            FROM marts.mart_summary
            WHERE occupation_group IS NOT NULL
            ORDER BY occupation_group;
        """
        params = None
    else:
        query = """
            SELECT DISTINCT occupation_group
            FROM marts.mart_summary
            WHERE occupation_group IS NOT NULL
                AND occupation_field = ?
            ORDER BY occupation_group;
        """
        params = (occupation_field,)

    return fetch_data_from_db(query, params)["occupation_group"].dropna().tolist()

# Returns the selected occupation field and group(s) from the sidebar,
# formatted for visual display (no quotes, readable format).
def get_selected_occupation_filters():
    # Get the occupation field choice directly from session_state
    occupation_field_choice = st.session_state.get("occupation_field_choice", "All occupation fields")
    all_fields = occupation_field_choice == "All occupation fields"

    # For fields, if not "All occupation fields", use it as a single-item list
    formatted_field_list = [] if all_fields else [occupation_field_choice]
    formatted_field_string = occupation_field_choice if not all_fields else ""

    # For groups, get the list from session state
    occupation_group_choices = st.session_state.get("occupation_group_choices", [])
    all_groups = len(occupation_group_choices) == 0  # empty = all groups

    formatted_group_list = occupation_group_choices
    formatted_group_string = ", ".join(formatted_group_list)

    return {
        "field_list": formatted_field_list,
        "group_list": formatted_group_list,
        "field_string": occupation_field_choice if not all_fields else "",
        "group_string": formatted_group_string,
        "all_fields": all_fields,
        "all_groups": all_groups,
    }

def display_occupation_choices():
    # Get the selected filters
    filters = get_selected_occupation_filters()

    # Map the correct emoji to each field
    FIELD_EMOJIS = {
        "Administration, ekonomi, juridik": "💼",
        "Försäljning, inköp, marknadsföring": "💹",
        "Hälso- och sjukvård": "🏥",
    }

    field_list = filters["field_list"]
    group_list = filters["group_list"]
    all_fields = filters["all_fields"]
    all_groups = filters["all_groups"]

    st.subheader("Showing data for:")

    col1, col2 = st.columns([1, 1])

    # --- Column 1: Occupation Field ---
    with col1:
        if all_fields:
            st.markdown("**All fields**")
        else:
            # Add emoji to field name if available
            display_fields = [
                f"{FIELD_EMOJIS.get(f, '')} {f}" if FIELD_EMOJIS.get(f) else f
                for f in field_list
            ]
            st.markdown(f"{', '.join(display_fields)}", unsafe_allow_html=True)

    # --- Column 2: Occupation Group ---
    with col2:
        if all_groups:
            st.markdown("**All groups**")
        else:
            shown_groups = group_list[:3]
            extra_count = len(group_list) - len(shown_groups)
            shown_text = ", ".join(shown_groups)
            if extra_count > 0:
                shown_text += f" +{extra_count}"
            st.markdown(f"**Group(s):** {shown_text}")

def display_dynamic_heading():
    # Get the selected filters
    filters = get_selected_occupation_filters()

    # Emoji mappings
    FIELD_EMOJIS = {
        "Administration, ekonomi, juridik": "💼",
        "Försäljning, inköp, marknadsföring": "💹",
        "Hälso- och sjukvård": "🏥",
    }

    PAGE_EMOJIS = {
        "Occupation Trends Over Time": "📈",
        "Geographical Coverage": "🌍",
        "Top Occupations": "🏆",
        "Top Occupations & Employers": "🏆",
        "Summary": "🗃️",
    }

    # Get selections
    field_list = filters["field_list"]
    group_list = filters["group_list"]
    all_fields = filters["all_fields"]
    all_groups = filters["all_groups"]

    selected_page = st.session_state.get("page_selection", "")
    page_emoji = PAGE_EMOJIS.get(selected_page, "")
    page_title = selected_page.replace("&", "and")  # Fallback

    # ---------- Header Construction ----------
    if all_fields and all_groups:
        # Case A: All fields and groups
        st.header(f"{page_emoji} {page_title} for all fields and groups", divider=True)

    elif not all_fields and all_groups:
        # Case B: Field selected, all groups
        field = field_list[0]
        field_emoji = FIELD_EMOJIS.get(field, "")
        st.header(f"{page_emoji}{field_emoji} {page_title} for {field}", divider=True)

    elif not all_fields and not all_groups:
        # Case C: Field and group(s) selected
        field = field_list[0]
        field_emoji = FIELD_EMOJIS.get(field, "")
        st.header(f"{page_emoji}{field_emoji} {page_title} for {field}", divider=True)

        shown_groups = group_list[:3]
        extra_count = len(group_list) - len(shown_groups)
        shown_text = ", ".join(shown_groups)
        if extra_count > 0:
            shown_text += f" +{extra_count}"
        st.markdown(f"**Group(s):** {shown_text}")

    elif all_fields and not all_groups:
        # Case E: All fields, but group(s) selected
        st.header(f"{page_emoji} {page_title} for selected groups", divider=True)

        shown_groups = group_list[:3]
        extra_count = len(group_list) - len(shown_groups)
        shown_text = ", ".join(shown_groups)
        if extra_count > 0:
            shown_text += f" +{extra_count}"
        st.markdown(f"**Group(s):** {shown_text}")

def set_background(current_page):
    # Set bg image based on current page
    asset_folder = "dashboard/assets"
    if current_page == "Occupation Trends":
        image_path = f"{asset_folder}/occ-trends.jpg"
    elif current_page == "Geographical Coverage":
        image_path = f"{asset_folder}/geo-coverage.jpg"
    elif current_page == "Top Occupations & Employers":
        image_path = f"{asset_folder}/top-occ-empl.jpg"
    else:
        image_path = f"{asset_folder}/dash-bg.jpg"

    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-attachment: fixed;
            background-size: cover;
            background-repeat: no-repeat;
            background-position: top center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )