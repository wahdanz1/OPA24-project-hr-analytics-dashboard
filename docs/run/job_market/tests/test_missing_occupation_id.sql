select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      -- Detects rows with missing occupation identifiers,
-- which are necessary for classification and analysis.

SELECT 
    * 
FROM "job_ads"."refined"."fct_job_ads" f 
LEFT JOIN "job_ads"."refined"."dim_occupation" d
    ON f.occupation_id = d.occupation_id 
WHERE d.occupation_id IS NULL
      
    ) dbt_internal_test