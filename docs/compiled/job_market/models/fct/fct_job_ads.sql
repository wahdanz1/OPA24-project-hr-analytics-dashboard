WITH  __dbt__cte__src_job_ads as (
WITH stg_job_ads AS (SELECT * FROM "job_ads"."staging"."job_ads")

SELECT 
    publication_date,
    id, -- dim_job_details ID
    occupation__label AS occupation, -- dim_occupation ID
    employer__name AS employer_name, -- dim_employer ID
    employer__workplace AS employer_workplace, -- dim_employer ID
    workplace_address__municipality AS workplace_municipality, -- dim_employer ID
    experience_required, -- dim_aux ID
    driving_license_required AS driver_license, -- dim_aux ID
    access_to_own_car, -- dim_aux ID
    number_of_vacancies AS vacancies,
    relevance, 
    application_deadline
FROM stg_job_ads
), fct_job_ads AS (SELECT * FROM __dbt__cte__src_job_ads)

SELECT 
    publication_date,
    md5(cast(coalesce(cast(id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))
    AS job_details_id,
    md5(cast(coalesce(cast(occupation as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))
    AS occupation_id,
    md5(cast(coalesce(cast(employer_name as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(employer_workplace as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(workplace_municipality as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))
    AS employer_id,
    md5(cast(coalesce(cast(experience_required as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(driver_license as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(access_to_own_car as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))
    AS aux_id,
    vacancies,
    relevance, 
    application_deadline
FROM fct_job_ads