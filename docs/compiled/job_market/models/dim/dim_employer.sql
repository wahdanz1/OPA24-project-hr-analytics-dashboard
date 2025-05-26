WITH  __dbt__cte__src_employer as (
WITH stg_job_ads AS (SELECT * FROM "job_ads"."staging"."job_ads")

SELECT
    employer__name AS employer_name,
    employer__workplace AS employer_workplace,
    employer__organization_number AS employer_org_number,
    workplace_address__street_address AS workplace_street_address,
    workplace_address__region AS workplace_region,
    workplace_address__municipality AS workplace_municipality,
    workplace_address__postcode AS workplace_postcode,
    workplace_address__city AS workplace_city,
    workplace_address__country AS workplace_country
FROM stg_job_ads
), src_employer AS (
    SELECT * FROM __dbt__cte__src_employer
)

SELECT DISTINCT
    md5(cast(coalesce(cast(employer_name as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(employer_workplace as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(workplace_municipality as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS employer_id,

    employer_name,
    employer_workplace,
    employer_org_number,
    workplace_street_address,
    workplace_region,
    workplace_municipality,
    workplace_postcode,
    
    upper(left(workplace_city, 1)) || lower(substring(workplace_city, 2))
 AS workplace_city,
    workplace_country

FROM src_employer