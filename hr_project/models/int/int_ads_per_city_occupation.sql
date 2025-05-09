-- This intermediate model is used to analyze the number of job ads per city and occupation.
-- It is used to analyze the most common (top 3) occupations in each city.
WITH fct_job_ads AS (SELECT * FROM {{ ref('fct_job_ads') }})
SELECT
    ja.publication_date,
    e.workplace_municipality,
    e.workplace_city,
    o.occupation,
    o.occupation_field,
    COUNT(DISTINCT ja.job_details_id) AS job_ad_count
    FROM fct_job_ads ja
    
    JOIN refined.dim_employer e
        ON e.employer_id = ja.employer_id
    JOIN refined.dim_occupation o
        ON o.occupation_id = ja.occupation_id

    GROUP BY e.workplace_municipality, e.workplace_city, o.occupation, o.occupation_field, ja.publication_date