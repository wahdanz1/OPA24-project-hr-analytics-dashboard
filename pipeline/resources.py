import dlt
import requests
import json

# To be able to import config.py and access its variables
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import variables from config.py
from config import base_url


# ---------- RESOURCE FUNCTIONS ----------
# --- Function for yield job ads ---
@dlt.resource(write_disposition="append")
def jobsearch_resource(params):
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
            break

        # Update the offset to fetch the next page of results
        offset += limit

# --- Helper function for making a GET request to the API ---
def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}  # Request JSON response
    response = requests.get(url_for_search, headers=headers, params=params) # Send GET request with parameters
    response.raise_for_status() # Raise an error for failed requests (non-2xx HTTP status)
    return json.loads(response.content.decode("utf8")) # Decode the JSON response into a dictionary



# --- For testing purposes ---
if __name__ == "__main__":
    print(base_url)
