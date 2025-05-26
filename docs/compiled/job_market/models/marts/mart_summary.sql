WITH fct AS (
    SELECT * FROM "job_ads"."refined"."fct_job_ads"
),

dim_occ AS (
    SELECT * FROM "job_ads"."refined"."dim_occupation"
),

dim_aux AS (
    SELECT * FROM "job_ads"."refined"."dim_aux"
),

dim_emp AS (
    SELECT * FROM "job_ads"."refined"."dim_employer"
)

SELECT 
    f.publication_date,
    f.vacancies,
    f.relevance,
    f.application_deadline,

    -- Occupation info
    o.occupation,
    o.occupation_group,
    o.occupation_field,

    -- Employer info
    e.employer_name,
    e.employer_workplace,
    e.workplace_municipality,
    e.workplace_region,

    -- Experience + aux info
    a.experience_required,
    a.driver_license,
    a.access_to_own_car

FROM fct f
LEFT JOIN dim_occ o ON f.occupation_id = o.occupation_id
LEFT JOIN dim_aux a ON f.aux_id = a.auxiliary_attributes_id
LEFT JOIN dim_emp e ON f.employer_id = e.employer_id