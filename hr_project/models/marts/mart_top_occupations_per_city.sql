-- This model shows the top 3 occupations per city.
-- It is used to analyze the most common occupations in each city.
WITH int_ads_per_city_occupation AS (SELECT * FROM {{ ref('int_ads_per_city_occupation') }})
SELECT
    workplace_municipality,
    workplace_city,
    occupation,
    occupation_field,
    job_ad_count,
    ROW_NUMBER() OVER (PARTITION BY workplace_municipality, workplace_city ORDER BY job_ad_count DESC) AS rank
    FROM int_ads_per_city_occupation apco

    QUALIFY rank <= 3