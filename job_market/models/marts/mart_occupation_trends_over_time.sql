WITH fct AS (
    SELECT * FROM {{ ref('fct_job_ads') }}
),

dim_aux AS (
    SELECT * FROM {{ ref('dim_aux') }}
),

dim_occupation AS (
    SELECT * FROM {{ ref('dim_occupation') }}
)

SELECT 
    fct.publication_date,
    fct.vacancies,
    aux.experience_required,
    occ.occupation,
    occ.occupation_group,
    occ.occupation_field
FROM fct
JOIN dim_aux aux ON aux.auxiliary_attributes_id = fct.aux_id
JOIN dim_occupation occ ON occ.occupation_id = fct.occupation_id
