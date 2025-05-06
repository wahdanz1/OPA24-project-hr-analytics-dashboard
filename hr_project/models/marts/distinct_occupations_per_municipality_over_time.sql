-- This model counts the number of distinct occupations per municipality over time.
-- It is used to analyze the distribution of job ads across different municipalities
-- and the variety of occupations available in each area.
SELECT
    e.workplace_municipality,
    COUNT(DISTINCT ja.occupation_id) AS distinct_occupations,
    DATE_TRUNC('week', ja.publication_date) AS week
    FROM refined.fct_job_ads ja
    
    JOIN refined.dim_employer e
        ON e.employer_id = ja.employer_id
    
    WHERE workplace_municipality IS NOT NULL
    AND ja.publication_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')

    GROUP BY e.workplace_municipality, week
    ORDER BY week, e.workplace_municipality