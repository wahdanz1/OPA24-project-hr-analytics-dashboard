WITH  __dbt__cte__src_aux as (
WITH stg_job_ads AS (SELECT * FROM "job_ads"."staging"."job_ads")

SELECT
    experience_required,
    driving_license_required AS driver_license,
    access_to_own_car
FROM stg_job_ads
), src_aux AS (SELECT * FROM __dbt__cte__src_aux)
SELECT DISTINCT
    md5(cast(coalesce(cast(experience_required as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(driver_license as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(access_to_own_car as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS auxiliary_attributes_id,
    experience_required,
    driver_license,
    access_to_own_car
FROM
    src_aux
WHERE
    experience_required IS NOT NULL
    OR driver_license IS NOT NULL
    OR access_to_own_car IS NOT NULL