-- Checks for any job ads with a publication date set in the future,
-- which could indicate incorrect or dirty data.

SELECT
    *
FROM {{ ref('src_job_ads') }}
WHERE CAST(publication_date AS DATE) > CURRENT_DATE