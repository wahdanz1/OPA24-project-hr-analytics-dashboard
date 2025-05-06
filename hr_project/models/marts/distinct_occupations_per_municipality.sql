-- This model counts the number of distinct occupations per municipality.
-- It is used to analyze the distribution of job ads across different municipalities
SELECT
    e.workplace_municipality,
    COUNT(DISTINCT ja.occupation_id) AS distinct_occupations
    FROM refined.fct_job_ads ja
    
    JOIN refined.dim_employer e
        ON e.employer_id = ja.employer_id
    
    WHERE workplace_municipality IS NOT NULL

    GROUP BY e.workplace_municipality
    ORDER BY distinct_occupations DESC