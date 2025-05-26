
  
  create view "job_ads"."refined"."dim_job_details__dbt_tmp" as (
    WITH  __dbt__cte__src_job_details as (
WITH stg_job_ads AS (SELECT * FROM "job_ads"."staging"."job_ads")

SELECT 
    id,
    headline,
    description__text AS description,
    description__text_formatted AS description_html_formatted,
    employment_type__label AS employment_type,
    duration__label AS duration,
    salary_type__label AS salary_type,
    scope_of_work__min AS scope_of_work_min,
    scope_of_work__max AS scope_of_work_max
FROM 
    stg_job_ads
), src_job_details AS (SELECT * FROM __dbt__cte__src_job_details)

SELECT DISTINCT
    md5(cast(coalesce(cast(id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS job_details_id,
    headline,
    description,
    description_html_formatted,
    employment_type,
    duration,
    salary_type,
    scope_of_work_min,
    scope_of_work_max
FROM 
    src_job_details
  );
