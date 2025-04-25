import dlt
from resources import fetch_job_ads



def create_pipeline():
    pipeline = dlt.pipeline(
        name="HR_Data_Pipeline",
        destination= dlt.destinations.duckdb("../hr_project/hr_job_ads.duckdb"),
        dataset_name="staging",
    )
    return pipeline

def run_pipeline():

    pipeline = create_pipeline()
    offset = 0  
    while offset < 500:
        data = fetch_job_ads(100,offset=offset)
        
        hits = data.get("hits",[])
        if hits:
            pipeline.run(fetch_job_ads(100,offset=offset))

        
        
        offset += 100
        print("awd")
        



if __name__ == "__main__":
    print("AWdaws")
    run_pipeline()