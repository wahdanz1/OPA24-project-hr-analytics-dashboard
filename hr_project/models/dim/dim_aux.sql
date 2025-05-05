{{ config(materialized = 'table') }} 

WITH src_aux AS (
    SELECT * FROM {{ ref('src_aux') }}
)
SELECT
    DISTINCT {{ dbt_utils.generate_surrogate_key(
        [
        'experience_required',
        'driver_license',
        'access_to_own_car'
    ]
    ) }} AS auxilliary_attributes_id,
    experience_required,
    driver_license,
    access_to_own_car
FROM
    src_aux
WHERE
    experience_required IS NOT NULL
    OR driver_license IS NOT NULL
    OR access_to_own_car IS NOT NULL