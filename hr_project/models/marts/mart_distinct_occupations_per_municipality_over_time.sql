-- This model counts the number of distinct occupations per municipality over time.
-- It is used to analyze the distribution of job ads across different municipalities
-- and the variety of occupations available in each area.
WITH fct_job_ads AS (SELECT * FROM {{ ref('fct_job_ads') }})
SELECT
    e.workplace_municipality,
    COUNT(DISTINCT ja.occupation_id) AS distinct_occupations,
    DATE_TRUNC('day', ja.publication_date) AS day
    FROM fct_job_ads ja
    
    JOIN refined.dim_employer e
        ON e.employer_id = ja.employer_id
    
    WHERE workplace_municipality IS NOT NULL
    AND ja.publication_date >= DATE_TRUNC('day', CURRENT_DATE - INTERVAL '2 weeks')

    GROUP BY e.workplace_municipality, day
    ORDER BY day, e.workplace_municipality