--trends over time Mart
SELECT publication_date,
       vacancies,
       experience_required,
       occupation,
       occupation_group,
       occupation_field
FROM refined.fct_job_ads
JOIN refined.dim_aux 
ON refined.dim_aux.auxiliary_attributes_id = refined.fct_job_ads.aux_id
JOIN refined.dim_occupation 
ON refined.dim_occupation.occupation_id = refined.fct_job_ads.occupation_id