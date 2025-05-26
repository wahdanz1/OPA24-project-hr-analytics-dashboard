with __dbt__cte__src_job_ads as (
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
) -- Checks for any job ads with a publication date set in the future,
-- which could indicate incorrect or dirty data.

SELECT
    *
FROM __dbt__cte__src_job_ads
WHERE CAST(publication_date AS DATE) > CURRENT_DATE