from pathlib import Path

base_url = "https://jobsearch.api.jobtechdev.se"

default_limit = 100
default_offset = 0
table_name = "job_ads"

occupation_field_list = [
    "X82t_awd_Qyc",  # Administration, ekonomi, juridik
    "RPTn_bxG_ExZ",  # Försäljning, inköp, marknadsföring
    "NYW6_mP6_vwf",  # Hälso- och sjukvård
]

working_directory = Path(__file__).resolve().parent

db_filename = "hr_job_ads.duckdb" # Database file name
dbt_folder = "hr_project" # Database file directory
db_path = working_directory / dbt_folder / db_filename  # Full path to the database file