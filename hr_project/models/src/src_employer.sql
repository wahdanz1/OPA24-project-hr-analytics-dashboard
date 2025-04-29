WITH stg_job_ads AS (SELECT * FROM {{ source('hr_job_ads', 'stg_ads') }})

SELECT
    employer__name AS employer_name,
    employer__workplace AS employer_workplace,
    employer__organization_number AS employer_org_number,
    workplace_address__street_address AS workplace_street_address,
    workplace_address__municipality AS workplace_municipality,
    workplace_address__postcode AS workplace_postcode,
    workplace_address__city AS workplace_city,
    workplace_address__country AS workplace_country
FROM stg_job_ads