-- Fails if driver_license is not required when access_to_own_car is required

SELECT *
FROM {{ ref('dim_aux') }}
WHERE access_to_own_car = True
  AND driver_license = False