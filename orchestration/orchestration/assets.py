########################
#        Setup         #
########################

# Import necessary Dagster packages
import dagster as dg

from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets

import dlt

# To be able to import config.py and access its variables
import sys
from pathlib import Path

# Add the parent directory (root, 2 levels up) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Import necessary functions/variables
from pipeline.resources import jobsearch_source
from config import db_path, dbt_path, profiles_dir
from pipeline.utils import make_params_list


############################
#        dlt asset         #
############################

dlt_resource = DagsterDltResource()

@dlt_assets(
    dlt_source=jobsearch_source(make_params_list(day_range=3)),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="job_ads_pipeline",
        destination=dlt.destinations.duckdb(str(db_path)),
        dataset_name="staging",
    ),
    group_name = "staging"
)
def job_ads_dlt_asset(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


############################
#         dbt asset        #
############################

dbt_project = DbtProject(
    project_dir = dbt_path,
    profiles_dir = profiles_dir
)

dbt_resource = DbtCliResource(project_dir = dbt_project)

# Prepare the manifest
dbt_project.prepare_if_dev()

@dbt_assets(
    manifest = dbt_project.manifest_path,
)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context = context).stream()
