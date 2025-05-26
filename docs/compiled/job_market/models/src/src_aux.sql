WITH stg_job_ads AS (SELECT * FROM "job_ads"."staging"."job_ads")

SELECT
    experience_required,
    driving_license_required AS driver_license,
    access_to_own_car
FROM stg_job_ads