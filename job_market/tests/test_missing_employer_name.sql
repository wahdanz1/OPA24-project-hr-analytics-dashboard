-- Flags records where `employer_name` is missing
-- or null — important for attribution and insights.

SELECT
    *
FROM {{ source('job_ads', 'stg_ads') }}
WHERE TRIM(employer__name) = '' OR employer__name IS NULL
