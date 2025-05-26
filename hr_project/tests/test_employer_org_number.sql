SELECT 
    * 
FROM {{ref('dim_employer')}}
WHERE LENGTH(employer_org_number) != 10