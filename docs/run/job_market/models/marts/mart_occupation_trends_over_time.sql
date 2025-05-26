
  
    
    

    create  table
      "job_ads"."marts"."mart_occupation_trends_over_time__dbt_tmp"
  
    as (
      WITH fct AS (
    SELECT * FROM "job_ads"."refined"."fct_job_ads"
),

dim_aux AS (
    SELECT * FROM "job_ads"."refined"."dim_aux"
),

dim_occupation AS (
    SELECT * FROM "job_ads"."refined"."dim_occupation"
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
    );
  
  