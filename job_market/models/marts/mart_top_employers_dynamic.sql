WITH fct_job_ads AS (
    SELECT * FROM {{ ref('fct_job_ads') }}
),

job_ads_enriched AS (
    SELECT
        ja.publication_date,
        o.occupation,
        o.occupation_group,
        o.occupation_field,
        ja.vacancies
    FROM fct_job_ads ja

    JOIN refined.dim_occupation o
        ON o.occupation_id = ja.occupation_id
)

SELECT
    publication_date,
    occupation,
    occupation_group,
    occupation_field,
    SUM(vacancies) AS total_vacancies
FROM job_ads_enriched
GROUP BY
    publication_date,
    occupation,
    occupation_group,
    occupation_field
