import dlt
from resources import fetch_job_ads



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
    pipeline.run(fetch_job_ads(
                    generate_parameters()
    ))
    print("Fetched 100 rows")
    
        
#Returns parameters for Occupational fields required Limit and offset input
def generate_parameters(limit = 100,offset = 0):
    # Codes related to Occupational Fields for jobtech API
    occupation_fields = [
        "X82t_awd_Qyc",
        "NYW6_mP6_vwf",
        "RPTn_bxG_ExZ"
    ]
    params = {

        "ocupation-field": occupation_fields,
        "limit":limit,
        "offset":offset
    }
    return params



if __name__ == "__main__":
    print("AWdaws")
    run_pipeline()