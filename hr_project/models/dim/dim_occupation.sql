
WITH src_occupation AS (SELECT * FROM {{ ref("src_occupation") }})

SELECT 
    {{dbt_utils.generate_surrogate_key(['id'])}} AS occupation_id,
    occupation,
    occupation_group,
    occupation_field
FROM src_occupation
