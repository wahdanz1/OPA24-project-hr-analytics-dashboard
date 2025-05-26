
  
    
    

    create  table
      "job_ads"."marts"."mart_top_employers__dbt_tmp"
  
    as (
      WITH fct_job_ads AS (
    SELECT * FROM "job_ads"."refined"."fct_job_ads"
),
dim_employer AS (
    SELECT * FROM "job_ads"."refined"."dim_employer"
),
dim_occupation AS (
    SELECT * FROM "job_ads"."refined"."dim_occupation"
)

SELECT
    dim_employer.employer_name,
    dim_employer.workplace_region,
    dim_occupation.occupation,
    SUM(fct_job_ads.vacancies) AS total_vacancies,
FROM fct_job_ads 
JOIN dim_employer 
    ON dim_employer.employer_id = fct_job_ads.employer_id
JOIN dim_occupation
    ON dim_occupation.occupation_id = fct_job_ads.occupation_id
GROUP BY
    dim_employer.employer_name,
    dim_employer.workplace_region,
    dim_occupation.occupation,
ORDER BY total_vacancies DESC
    );
  
  