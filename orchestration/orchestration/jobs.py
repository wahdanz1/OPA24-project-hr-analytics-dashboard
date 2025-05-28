import dagster as dg 


########################
#         Jobs         #
########################

job_dlt = dg.define_asset_job(
    name="dlt_job",
    selection= dg.AssetSelection.keys("dlt_jobsearch_source_jobsearch_resource"),
)

job_dbt = dg.define_asset_job(
    name="dbt_job",
    selection= dg.AssetSelection.groups("dbt"),
)