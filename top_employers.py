import streamlit as st 
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart

def top_employers_per_occupation():
    st.write()