WITH stg_job_ads AS (SELECT * FROM {{ source('hr_job_ads', 'stg_ads') }})

SELECT 
    occupation__label,
    id,
    employer__name AS employer_name, 
    employer__workplace AS employer_workplace,
    workplace_address__municipality AS workplace_municipality,
    number_of_vacancies AS vacancies,
    relevance, 
    application_deadline
FROM stg_job_ads
