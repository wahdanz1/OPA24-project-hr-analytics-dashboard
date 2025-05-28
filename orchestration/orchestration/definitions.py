from dagster import Definitions, load_assets_from_modules
from . import assets

all_assets = load_assets_from_modules([assets])

from .assets import dlt_resource,dbt_resource
from .jobs import job_dbt,job_dlt
from .schedules import schedule_dlt
from .sensors import dlt_load_sensor

defs = Definitions(
    assets=all_assets,
    resources={
        "dlt": dlt_resource,
        "dbt": dbt_resource
    },
    jobs=[job_dlt, job_dbt],
    schedules=[schedule_dlt],
    sensors=[dlt_load_sensor],
)
