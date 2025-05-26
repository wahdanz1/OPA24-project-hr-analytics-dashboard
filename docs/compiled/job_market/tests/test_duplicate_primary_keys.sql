-- Ensures no duplicate primary keys exist in key models,
-- which could compromise downstream joins and analysis.

SELECT 
    id, 
    COUNT(*) 
FROM "job_ads"."staging"."job_ads" 
GROUP BY id 
HAVING COUNT(*) > 1