-- This model counts the number of distinct occupations per municipality.
-- It is used to analyze the distribution of job ads across different municipalities
WITH fct_job_ads AS (
    SELECT * FROM {{ ref('fct_job_ads') }}
)

SELECT
    ja.publication_date,
    e.workplace_municipality,
    o.occupation_field,
    COUNT(DISTINCT ja.occupation_id) AS distinct_occupations
FROM fct_job_ads ja

JOIN refined.dim_employer e
    ON e.employer_id = ja.employer_id
JOIN refined.dim_occupation o
    ON o.occupation_id = ja.occupation_id

WHERE workplace_municipality IS NOT NULL

GROUP BY ja.publication_date, e.workplace_municipality, o.occupation_field