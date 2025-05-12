WITH int_ads_per_employer_occupation AS (SELECT * FROM {{ ref('int_ads_per_employer_occupation') }})
SELECT 
    occupation,
    employer_name,
    occupation_field, 
    total_vacancies,
FROM int_ads_per_employer_occupation 
