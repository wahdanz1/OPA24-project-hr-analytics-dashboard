import dagster as dg
from .jobs import job_dbt

############################
#         Sensors          #
############################
@dg.asset_sensor(asset_key=dg.AssetKey("dlt_jobsearch_source_jobsearch_resource"),
                 job=job_dbt)
def dlt_load_sensor():
    yield dg.RunRequest()