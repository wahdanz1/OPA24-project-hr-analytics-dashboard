from pathlib import Path

# Base URL for the JobTech API
base_url = "https://jobsearch.api.jobtechdev.se"

# Endpoint parameters
default_limit = 100
default_offset = 0

# Occupation field dictionary mapping
occupation_field_dict = {
    "Administration, ekonomi, juridik"   : "X82t_awd_Qyc",  
    "Försäljning, inköp, marknadsföring" : "RPTn_bxG_ExZ",
    "Hälso- och sjukvård"                : "NYW6_mP6_vwf",  
}

# Directory of the config.py file
working_directory = Path(__file__).resolve().parent

# Database configuration
table_name = "job_ads"

dbt_folder = "job_market" # Database file directory
dbt_path = working_directory / dbt_folder  # Path to the database folder
db_filename = "job_ads.duckdb" # Database file name
db_path = working_directory / dbt_folder / db_filename  # Full path to the database file

profiles_dir = Path.home() / ".dbt"
