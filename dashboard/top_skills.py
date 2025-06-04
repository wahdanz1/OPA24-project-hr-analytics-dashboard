import streamlit as st
import pandas as pd
from .utils import fetch_data_from_db
from .plots import create_pie_chart

# To be able to import gemini
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import gemini
from ai.gemini import GeminiHandler
from ai.gemini_analyze_description import get_top_skills

def top_skills_page():
    st.header("🛠️ Top Skills & Experiences", divider=True)

    # Get the raw sidebar selections
    occupation_group_choices = st.session_state.get("occupation_group_choices", [])
    
    # Import environment variables
    from pathlib import Path
    from dotenv import dotenv_values

    # Explicitly load .env from project root
    env_path = Path(__file__).resolve().parent.parent / ".env"
    env_vars = dotenv_values(dotenv_path=env_path)
    gemini_api_key = env_vars.get("GEMINI_API_KEY")

    # See if the Gemini API key ("GEMINI_API_KEY") is set in the .env file
    if not gemini_api_key:
        # If not set, show a warning message
        st.warning("Gemini API key is not set. Please check your environment variables.")
        return
    else:
        # Show Dataframe + Pie Chart only if an occupation group is selected (not "All")
        if occupation_group_choices:
            st.subheader(f"{', '.join(occupation_group_choices)}")
            # Based on selected occupation group and region, build a query
            top_skill_query = f"""
                SELECT
                    description
                FROM refined.fct_job_ads ja
                JOIN refined.dim_occupation o ON ja.occupation_id = o.occupation_id
                JOIN refined.dim_job_details jd ON ja.job_details_id = jd.job_details_id
                JOIN refined.dim_employer e ON ja.employer_id = e.employer_id
                WHERE occupation_group IN ({', '.join(f"'{group}'" for group in occupation_group_choices)})
                ORDER BY publication_date DESC
                LIMIT 100
            """

            # Fetch the data from the database
            top_skill_data = fetch_data_from_db(top_skill_query)

            # Check if the data is not empty
            if not top_skill_data.empty:
                # Check that it has at least 10 lines
                if len(top_skill_data) >= 10:

                    with st.spinner("Gemini is analyzing the data..."):
                        # Let Gemini analyze the dataframe and return the top skills
                        top_5_skills = get_top_skills(top_skill_data)

                        # Filter the top 10 skills
                        top_5_skills = top_5_skills.head(10)

                        col1, col2 = st.columns(2)

                        # Column 1 - Display the DataFrame with the columns [skill] and [total_occurences]
                        with col1:
                            st.subheader("Top 10")
                            st.dataframe(top_5_skills, use_container_width=True, hide_index=True)

                        # Column 2 - Display the Pie chart
                        with col2:
                            st.subheader("Distribution")
                            pie_chart = create_pie_chart(
                                data=top_5_skills,
                                title=" ",
                                values="Count",
                                names="Skill",
                            )
                            st.plotly_chart(pie_chart, use_container_width=True)

                        col2, col3 = st.columns(2)
                        # Column 1 - Display the query
                        with col2:
                            with st.expander(label="SQL Query"):
                                st.code(top_skill_query, language="sql", wrap_lines=True)

                        # Column 2 - Display the fetched data
                        with col3:
                            with st.expander(label="Data Preview"):
                                st.dataframe(top_skill_data)

                else:
                    st.markdown("There are too few job ads in this group/region. Please select a different occupation group or region.")
        else:
            st.markdown("Select an **occupation group** in the sidebar to display results.")

