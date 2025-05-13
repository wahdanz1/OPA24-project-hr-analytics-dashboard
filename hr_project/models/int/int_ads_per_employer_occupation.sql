WITH fct_job_ads AS (SELECT * FROM {{ ref('fct_job_ads') }})
SELECT
    e.employer_name,
    o.occupation,
    o.occupation_field,
    ja.publication_date,
    SUM(ja.vacancies) AS total_vacancies
    FROM fct_job_ads ja
    JOIN refined.dim_employer e
        ON e.employer_id = ja.employer_id
    JOIN refined.dim_occupation o
        ON o.occupation_id = ja.occupation_id
    GROUP BY o.occupation, e.employer_name, o.occupation_field, ja.publication_date