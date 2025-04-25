import dlt
import requests
import json

# X82t_awd_Qyc	Administration, ekonomi, juridik
# RPTn_bxG_ExZ	Försäljning, inköp, marknadsföring
# NYW6_mP6_vwf	Hälso- och sjukvård
occupation_field_list = ["X82t_awd_Qyc", "RPTn_bxG_ExZ", "NYW6_mP6_vwf"]

@dlt.resource(write_disposition="append")
def fetch_job_ads(ads_to_fetch=10, offset=0):
    # Endpoint url & parameters
    url = "https://jobsearch.api.jobtechdev.se/search"
    params = {
        "q": "occupation-field=" + ",".join(occupation_field_list),
        "size": ads_to_fetch,  # Number of job ads to fetch
        "offset": offset  # Offset for pagination
        }
    
    # Make the GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        yield data
    else:
        # Handle the error case
        print(f"Error status code: {response.status_code}")
        yield []


# For testing purposes
if __name__ == "__main__":
    print("Fetching job ads...")
    data = fetch_job_ads()
    for item in data:
        print(item)
