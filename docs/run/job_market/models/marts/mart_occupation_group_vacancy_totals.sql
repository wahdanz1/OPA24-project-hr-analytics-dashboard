
  
    
    

    create  table
      "job_ads"."marts"."mart_occupation_group_vacancy_totals__dbt_tmp"
  
    as (
      WITH fct AS (
    SELECT * FROM "job_ads"."refined"."fct_job_ads"
),

dim_employer AS (
    SELECT * FROM "job_ads"."refined"."dim_employer"
),

dim_occupation AS (
    SELECT * FROM "job_ads"."refined"."dim_occupation"
)

SELECT
    f.publication_date,
    e.workplace_region,
    e.workplace_municipality,
    o.occupation_group,
    o.occupation_field,
    SUM(f.vacancies) AS total_vacancies
FROM fct f
JOIN dim_employer e ON e.employer_id = f.employer_id
JOIN dim_occupation o ON o.occupation_id = f.occupation_id
WHERE e.workplace_region IS NOT NULL
    AND e.workplace_municipality IS NOT NULL
GROUP BY
    f.publication_date,
    e.workplace_region,
    e.workplace_municipality,
    o.occupation_group,
    o.occupation_field
    );
  
  