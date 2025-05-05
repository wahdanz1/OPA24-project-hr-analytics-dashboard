WITH src_employer AS (SELECT * FROM {{ ref('src_employer') }})

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['employer_name',
                                        'employer_workplace',
                                        'workplace_municipality'])
    }} AS employer_id,
    employer_name,
    employer_workplace,
    employer_org_number,
    workplace_street_address,
    workplace_region,
    workplace_municipality,
    workplace_postcode,
    workplace_city,
    workplace_country
FROM src_employer