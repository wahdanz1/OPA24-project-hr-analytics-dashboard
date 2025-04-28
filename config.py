import os 
from pathlib import Path


base_url = "https://jobsearch.api.jobtechdev.se/search"

default_limit = 100

occupation_field_list = [
    "X82t_awd_Qyc",  # Administration, ekonomi, juridik
    "RPTn_bxG_ExZ",  # Försäljning, inköp, marknadsföring
    "NYW6_mP6_vwf",  # Hälso- och sjukvård
]

working_directory = Path(__file__).resolve().parent

db_path = working_directory/"hr_project"/"hr_job_ads.duckdb"  # Full path to the database file