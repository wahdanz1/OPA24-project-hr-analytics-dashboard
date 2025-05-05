WITH fct_job_ads AS (SELECT * FROM {{ ref('src_job_ads') }})

SELECT 
    publication_date,
    {{ dbt_utils.generate_surrogate_key(['id']) }}
    AS job_details_id,
    {{ dbt_utils.generate_surrogate_key(['occupation']) }}
    AS occupation_id,
    {{ dbt_utils.generate_surrogate_key(['employer_name',
                                        'employer_workplace',
                                        'workplace_municipality']) }}
    AS employer_id,
    {{ dbt_utils.generate_surrogate_key(['experience_required',
                                        'driver_license',
                                        'access_to_own_car']) }}
    AS aux_id,
    vacancies,
    relevance, 
    application_deadline
FROM fct_job_ads