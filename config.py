from pathlib import Path

base_url = "https://jobsearch.api.jobtechdev.se"

default_limit = 100
default_offset = 0
table_name = "job_ads"

occupation_field_dict = {
    "Administration, ekonomi, juridik"   : "X82t_awd_Qyc",  
    "Försäljning, inköp, marknadsföring" : "RPTn_bxG_ExZ",
    "Hälso- och sjukvård"                : "NYW6_mP6_vwf",  
}



working_directory = Path(__file__).resolve().parent

db_filename = "job_ads.duckdb" # Database file name
dbt_folder = "job_market" # Database file directory
db_path = working_directory / dbt_folder / db_filename  # Full path to the database file