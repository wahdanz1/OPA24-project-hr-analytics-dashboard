import dagster as dg
from .assets import dbt_models, job_ads_dlt_asset

########################
#         Jobs         #
########################

dlt_job = dg.define_asset_job(
    name="dlt_job",
    selection = dg.AssetSelection.assets(*job_ads_dlt_asset.keys),
)

dbt_job = dg.define_asset_job(
    name ="dbt_job",
    selection = dg.AssetSelection.assets(*dbt_models.keys)
)