import dlt
from resources import fetch_job_ads



def create_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="HR_Data_Pipeline",
        destination= dlt.destinations.duckdb("hr_project/hr_job_ads.duckdb"),
        dataset_name="staging",
    )
    return pipeline

def run_pipeline():

    pipeline = create_pipeline()
    offset = 0  
    limit = 100
    while offset < 1900:
       
        pipeline.run(fetch_job_ads(limit,offset))

        offset += limit
        print("Fetched 100 rows")
        



if __name__ == "__main__":
    print("AWdaws")
    run_pipeline()