SELECT 
    id, 
    COUNT(*) 
FROM {{ source('hr_job_ads', 'stg_ads') }} 
GROUP BY id 
HAVING COUNT(*) > 1
