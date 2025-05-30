import dlt
import requests
import json
import time

# To be able to import config.py and access its variables
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import variables from config.py
from config import base_url


# ---------- RESOURCE FUNCTIONS ----------
# --- Function for yield job ads ---
@dlt.resource(write_disposition="merge", primary_key="id")
def jobsearch_resource(params_list):
    for params in params_list:
        url_for_search = f"{base_url}/search"
        limit = params.get("limit", 100)
        offset = params.get("offset", 0)

        while True:
            # Build the page's parameters, including offset and limit
            page_params = dict(params, offset=offset) # Add the current offset to the params

            # Get the data using the helper function
            data = _get_ads(url_for_search, page_params)

            hits = data.get("hits", []) # Extract the list of job ads

            # If there are no more hits, stop the loop (end of pagination)
            if not hits:
                break

            # Yield each job ad
            for ad in hits:
                yield ad
            
            # If fewer ads than the limit are returned (less than a full page), break the loop
            if len(hits) < limit or offset > 1900:
                if offset > 1900:
                        print(f"⚠️ Warning: reached 2000 hits - some ads might not have been fetched.")
                break
            
            # Print the number of ads fetched in this batch
            print(f"Fetched {len(hits)} ads...")

            # Update the offset to fetch the next page of results
            offset += limit

# --- Helper function for making a GET request to the API ---
def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}  # Request JSON response
    # Add a sleep to respect the endpoint
    sleep_time = 1
    time.sleep(sleep_time)  # Uncomment if you want to add a delay between requests
    response = requests.get(url_for_search, headers=headers, params=params) # Send GET request with parameters
    response.raise_for_status() # Raise an error for failed requests (non-2xx HTTP status)
    return json.loads(response.content.decode("utf8")) # Decode the JSON response into a dictionary

@dlt.source
def jobsearch_source(params_list):
    yield jobsearch_resource(params_list)

# --- For testing purposes ---
if __name__ == "__main__":
    print(base_url)
