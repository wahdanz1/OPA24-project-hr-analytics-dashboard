WITH fct_job_ads AS (
    SELECT * FROM "job_ads"."refined"."fct_job_ads"
),

dim_occupation AS (
    SELECT * FROM "job_ads"."refined"."dim_occupation"
)

SELECT
    fct_job_ads.publication_date,
    dim_occupation.occupation,
    dim_occupation.occupation_group,
    dim_occupation.occupation_field,
    SUM(fct_job_ads.vacancies) AS total_vacancies
FROM fct_job_ads
JOIN dim_occupation 
    ON dim_occupation.occupation_id = fct_job_ads.occupation_id
GROUP BY
    fct_job_ads.publication_date,
    dim_occupation.occupation,
    dim_occupation.occupation_group,
    dim_occupation.occupation_field,