def get_database_instructions() -> str:
    """
    Clear, precise instructions on all available tables & marts.
    Gemini should prefer the prebuilt marts when possible.
    """
    return """
AVAILABLE SCHEMAS & TABLES (refined.*)

■ FACT TABLE
• fct_job_ads
    • publication_date      (date)
    • job_details_id        (fk → dim_job_details.job_details_id)
    • occupation_id         (fk → dim_occupation.occupation_id)
    • employer_id           (fk → dim_employer.employer_id)
    • aux_id                (fk → dim_aux.auxiliary_attributes_id)
    • vacancies             (int)
    • relevance             (numeric)
    • application_deadline  (date)

■ DIMENSION TABLES
• dim_occupation
    • occupation_id (pk)
    • occupation
    • occupation_group
    • occupation_field

• dim_employer
    • employer_id
    • employer_name
    • employer_workplace
    • workplace_city
    • workplace_municipality
    • workplace_region
    • workplace_postcode
    • employer_org_number

• dim_aux
    • auxiliary_attributes_id
    • experience_required
    • driver_license
    • access_to_own_car

• dim_job_details
    • job_details_id
    • headline
    • description
    • employment_type
    • duration
    • salary_type
    • scope_of_work_min
    • scope_of_work_max

■ PREBUILT MARTS
Use these whenever they satisfy the user’s request. They save you from joins.

• mart_top_employers  
    • Columns: employer_name, workplace_region, occupation, total_vacancies  
    • Good for “top N employers” queries

• mart_top_occupations_dynamic  
    • Columns: publication_date, workplace_region, workplace_municipality, occupation, occupation_field, total_vacancies  
    • Good for “top N occupations” over time or by geography

• mart_occupation_trends_over_time  
    • Columns: publication_date, vacancies, experience_required, occupation, occupation_group, occupation_field  
    • Good for time-series “trend” plots

JOIN KEYS
• fct_job_ads.employer_id    = dim_employer.employer_id  
• fct_job_ads.occupation_id  = dim_occupation.occupation_id  
• fct_job_ads.aux_id         = dim_aux.auxiliary_attributes_id  
• fct_job_ads.job_details_id = dim_job_details.job_details_id  

GENERAL RULES
1. ALWAYS prefix tables & marts with `refined.`  
2. NEVER reference src_* or int_* models.  
3. Prefer a MART if it directly covers the user’s ask.  
4. When writing ad-hoc SQL, JOIN fact → dim tables using the above keys.  
5. Write each query on one line, no Markdown fences.  
6. For string filters, use `lower(col) = 'value'` or `ILIKE`.  

EXAMPLES
— Top 10 employers for sjuksköterska —
SELECT employer_name, total_vacancies
FROM refined.mart_top_employers
WHERE lower(occupation) = 'sjuksköterska'
ORDER BY total_vacancies DESC
LIMIT 10

— Trend of vacancies for nurse over time —
SELECT publication_date, vacancies
FROM refined.mart_occupation_trends_over_time
WHERE lower(occupation) = 'sjuksköterska'
ORDER BY publication_date

But make your you figure out the valid content of the SQL query
By using an exploratory query to find the right table and columns
"""
