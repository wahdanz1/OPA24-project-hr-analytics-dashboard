from dagster import Definitions, load_assets_from_modules
from . import assets

all_assets = load_assets_from_modules([assets])

from .assets import dlt_resource

defs = Definitions(
    assets=all_assets,
    resources={"dlt": dlt_resource},
)
