-- This model counts the number of distinct occupations.
-- It is used to analyze the distribution of job ads across different occupations.
SELECT 
    o.occupation,
    COUNT(DISTINCT ja.job_details_id) AS distinct_occupations,
    DATE_TRUNC('week', ja.publication_date) AS week
FROM refined.fct_job_ads ja

JOIN refined.dim_occupation o
    ON ja.occupation_id = o.occupation_id

WHERE ja.publication_date >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '6 weeks')

GROUP BY o.occupation, week
ORDER BY week, distinct_occupations DESC