import dagster as dg

############################
#         Sensors          #
############################

@dg.asset_sensor(
    asset_key=dg.AssetKey("dlt_jobsearch_source_jobsearch_resource"),
    job_name="dbt_job"
)
def dlt_load_sensor():
    yield dg.RunRequest()
