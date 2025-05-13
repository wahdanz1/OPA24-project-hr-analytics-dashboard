WITH fct_job_ads AS (
    SELECT * FROM {{ ref('fct_job_ads') }}
),

job_ads_enriched AS (
    SELECT
        ja.publication_date,
        e.workplace_region,
        e.workplace_municipality,
        o.occupation,
        o.occupation_field,
        ja.vacancies
    FROM fct_job_ads ja
    JOIN refined.dim_employer e
        ON e.employer_id = ja.employer_id
    JOIN refined.dim_occupation o
        ON o.occupation_id = ja.occupation_id
    WHERE e.workplace_region IS NOT NULL
        AND e.workplace_municipality IS NOT NULL
)

SELECT
    publication_date,
    workplace_region,
    workplace_municipality,
    occupation,
    occupation_field,
    SUM(vacancies) AS total_vacancies
FROM job_ads_enriched
GROUP BY
    publication_date,
    workplace_region,
    workplace_municipality,
    occupation,
    occupation_field
