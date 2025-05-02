WITH stg_job_ads AS (SELECT * FROM {{ source('hr_job_ads', 'stg_ads') }})

SELECT *
    experience_required,
    driving_license_required AS driver_license,
    access_to_own_car
FROM stg_job_ads