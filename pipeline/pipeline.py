import dlt
from resources import jobsearch_resource



# Creates a pipeline 
def create_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="HR_Data_Pipeline",
        destination= dlt.destinations.duckdb("hr_project/hr_job_ads.duckdb"),
        dataset_name="staging",
    )
    return pipeline
# Creates And Runs a pipeline
def run_pipeline():

    pipeline = create_pipeline()


    occupation_fields = [
        "X82t_awd_Qyc",
        "NYW6_mP6_vwf",
        "RPTn_bxG_ExZ"
    ]

    for field in occupation_fields:
        params = {
            "occupation-field": field,
            "limit":100,
            "offset":0,
        }
        pipeline.run(
                    jobsearch_resource(params),
                    table_name="job_ads"
                    )
    
    
    print("Completed Fetch")
    
        



if __name__ == "__main__":
    print("AWdaws")
    run_pipeline()