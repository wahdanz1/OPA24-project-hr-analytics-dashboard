SELECT *
FROM {{ source('hr_job_ads', 'stg_ads') }}
WHERE TRIM(employer__name) = '' OR employer__name IS NULL
