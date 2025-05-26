WITH  __dbt__cte__src_occupation as (
WITH stg_job_ads AS (SELECT * FROM "job_ads"."staging"."job_ads")

SELECT 
    occupation__concept_id AS occupation_id,
    occupation__label AS occupation,
    occupation_group__concept_id AS occupation_group_id, 
    occupation_group__label AS occupation_group,
    occupation_field__concept_id AS occupation_field_id,
    occupation_field__label AS occupation_field
FROM stg_job_ads
), src_occupation AS (SELECT * FROM __dbt__cte__src_occupation)

SELECT DISTINCT
    md5(cast(coalesce(cast(occupation as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS occupation_id,
    occupation,
    occupation_group,
    occupation_field
FROM src_occupation