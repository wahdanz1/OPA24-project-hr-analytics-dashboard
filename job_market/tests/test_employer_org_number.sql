-- Validates that all employer organization numbers are exactly 10 digits,
-- as expected by Swedish organization number standards.

SELECT 
    * 
FROM {{ref('dim_employer')}}
WHERE LENGTH(employer_org_number) != 10