WITH src_job_details AS (SELECT * FROM {{ ref('src_job_details') }})

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['id']) }} AS job_details_id,
    headline,
    description,
    description_html_formatted,
    employment_type,
    duration,
    salary_type,
    scope_of_work_min,
    scope_of_work_max
FROM 
    src_job_details
