WITH int_ads_per_employer_occupation AS (SELECT * FROM {{ ref('int_ads_per_employer_occupation') }})
SELECT 
    occupation,
    employer_name,
    ads_posted_last_30_days,
    RANK() OVER (PARTITION BY occupation ORDER BY ads_posted_last_30_days DESC) AS employer_rank
FROM int_ads_per_employer_occupation
QUALIFY employer_rank <= 10

