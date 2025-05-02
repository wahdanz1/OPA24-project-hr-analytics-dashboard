WITH stg_job_ads AS (SELECT * FROM {{ source('hr_job_ads', 'stg_ads') }})

SELECT 
    occupation__label, -- dim_occupation ID
    id, -- dim_job_details ID
    employer__name AS employer_name, -- dim_employer ID
    employer__workplace AS employer_workplace, -- dim_employer ID
    workplace_address__municipality AS workplace_municipality, -- dim_employer ID
    -- dim_aux ID
    number_of_vacancies AS vacancies,
    relevance, 
    application_deadline
FROM stg_job_ads
