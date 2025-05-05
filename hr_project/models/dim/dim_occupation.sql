WITH src_occupation AS (SELECT * FROM {{ ref('src_occupation') }})

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['occupation']) }} AS occupation_id,
    occupation,
    occupation_group,
    occupation_field
FROM src_occupation
