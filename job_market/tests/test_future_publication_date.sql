SELECT 
    * 
FROM {{ ref('src_job_ads') }} 
WHERE publication_date > CURRENT_DATE