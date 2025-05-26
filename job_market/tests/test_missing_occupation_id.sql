SELECT 
    * 
FROM {{ ref('fct_job_ads') }} f 
LEFT JOIN {{ ref('dim_occupation') }} d ON f.occupation_id = d.occupation_id 
WHERE d.occupation_id IS NULL