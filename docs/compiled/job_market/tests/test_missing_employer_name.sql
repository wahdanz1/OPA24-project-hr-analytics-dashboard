-- Flags records where `employer_name` is missing
-- or null — important for attribution and insights.

SELECT
    *
FROM "job_ads"."staging"."job_ads"
WHERE TRIM(employer__name) = '' OR employer__name IS NULL