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
        occupation_groups = occupation_group_choices
    else:
        occupation_groups = get_occupation_group_list(occupation_field_choice)

    occupation_group_string = ", ".join(f"'{group}'" for group in occupation_groups)

    # Get limit and interval values
    limit_value = st.session_state.get("sidebar_limit")
    interval_value = st.session_state.get("sidebar_interval")
    start_day, end_day = sorted(interval_value)
    requires_experience = st.session_state.get("sidebar_requires_experience")

    # Get region from session
    region_choice_raw = st.session_state.get("sidebar_region_choice", "All regions")

    if region_choice_raw == "All regions":
        all_regions = get_region_list(
            occupation_field=occupation_field_choice,
            occupation_groups=occupation_groups
        )
        region_string = ", ".join(f"'{region}'" for region in all_regions)
    else:
        region_string = f"'{region_choice_raw}'"

    return occupation_field_string, occupation_group_string, limit_value, start_day, end_day, requires_experience, region_string

# Function to get the list of occupation fields from the database
# Returns a list of unique occupation fields to be used in the sidebar
st.cache_data
def get_occupation_field_list():
    query = f"""
        SELECT
            DISTINCT occupation_field
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
            SELECT
                DISTINCT occupation_group
            FROM marts.mart_summary
            WHERE occupation_group IS NOT NULL
            ORDER BY occupation_group;
        """
        params = None
    else:
        query = """
            SELECT
                DISTINCT occupation_group
            FROM marts.mart_summary
            WHERE occupation_group IS NOT NULL
                AND occupation_field = ?
            ORDER BY occupation_group;
        """
        params = (occupation_field,)
    
    df = fetch_data_from_db(query, params)
    return df["occupation_group"].dropna().tolist() if not df.empty else []

# Function to get the list of regions from the database
# Returns a list of unique regions to be used in the sidebar
def get_region_list(
    occupation_field: str = "All occupation fields", occupation_groups: list = None) -> list:
    query = """
        SELECT DISTINCT workplace_region
        FROM marts.mart_summary
        WHERE workplace_region IS NOT NULL
    """
    params = []

    if occupation_field != "All occupation fields":
        query += " AND occupation_field = ?"
        params.append(occupation_field)

    if occupation_groups and "All occupation groups" not in occupation_groups:
        placeholders = ", ".join(["?"] * len(occupation_groups))
        query += f" AND occupation_group IN ({placeholders})"
        params.extend(occupation_groups)

    query += " ORDER BY workplace_region ASC;"

    df = fetch_data_from_db(query, params if params else None)
    return df["workplace_region"].dropna().tolist() if not df.empty else []

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

# Function for displaying dynamic heading (based on occupation field/group)
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
        "Summary": "🗃️",
        "Occupation Trends": "📈",
        "Geographical Coverage": "🌍",
        "Top Occupations & Employers": "🏆",
        "Top Skills & Experiences": "🛠️",
        "Interactive Assistant": "🤖",
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
        st.header(f"{field_emoji} {page_title} for {field}", divider=True)

    elif not all_fields and not all_groups:
        # Case C: Field and group(s) selected
        field = field_list[0]
        field_emoji = FIELD_EMOJIS.get(field, "")
        st.header(f"{field_emoji} {page_title} for {field}", divider=True)

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

def wrap_label(label, max_len=25):
    if len(label) <= max_len:
        return label
    # Split into words and insert <br> where needed
    words = label.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) <= max_len:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "<br>".join(lines)

# Function for setting the background on the different pages
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

# Method for building CSS-code dyamically (to not style certain elements on certain pages)
def build_css_code(current_page):
    from .css import prefix, header_styling, container_styling, element_container_styling, button_styling, suffix
    css_code = prefix
    if current_page != "Interactive Assistant":
        css_code += header_styling + container_styling + element_container_styling + button_styling
    else:
        css_code += header_styling + element_container_styling + button_styling

    css_code += suffix

    return css_code
