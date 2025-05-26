select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      -- Validates that all employer organization numbers are exactly 10 digits,
-- as expected by Swedish organization number standards.

SELECT 
    * 
FROM "job_ads"."refined"."dim_employer"
WHERE LENGTH(employer_org_number) != 10
      
    ) dbt_internal_test