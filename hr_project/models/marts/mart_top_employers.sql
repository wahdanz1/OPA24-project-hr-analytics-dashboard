WITH fct_job_ads AS (
    SELECT * FROM {{ ref('fct_job_ads') }}
)

SELECT
    e.employer_name,
    e.workplace_region,
    o.occupation,
    SUM(ja.vacancies) AS total_vacancies,
FROM fct_job_ads ja
JOIN refined.dim_employer e
    ON ja.employer_id = e.employer_id
JOIN refined.dim_occupation o
    ON ja.occupation_id = o.occupation_id
GROUP BY
    employer_name,
    workplace_region,
    occupation
ORDER BY total_vacancies DESC