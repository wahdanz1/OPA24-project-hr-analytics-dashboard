def get_database_instructions() -> str:
    """
    Clear, precise instructions on all available tables & marts.
    Gemini should prefer the prebuilt marts when possible.
    """
    return """
AVAILABLE OCCUPATION FIELDS
    - "Administration, ekonomi, juridik" 
    - "Försäljning, inköp, marknadsföring"
    - "Hälso- och sjukvård"

AVAILABLE SCHEMAS & TABLES (refined.*)

NOTE: All values are in Swedish, so never try to translate "Sjuksköterska" into "Nurse", for example.

FACT TABLE
fct_job_ads
- publication_date      (date)
- job_details_id        (fk → dim_job_details.job_details_id)
- occupation_id         (fk → dim_occupation.occupation_id)
- employer_id           (fk → dim_employer.employer_id)
- aux_id                (fk → dim_aux.auxiliary_attributes_id)
- vacancies             (int)
- relevance             (numeric)
- application_deadline  (date)

DIMENSION TABLES
dim_occupation
- occupation_id         (pk)
- occupation            (varchar)
- occupation_group      (varchar)
- occupation_field      (varchar)

dim_employer
- employer_id (pk)
- employer_name         (varchar)
- employer_workplace    (varchar)
- workplace_city        (varchar)
- workplace_municipality(varchar)
- workplace_region      (varchar)
- workplace_postcode    (varchar)
- employer_org_number   (varchar)

dim_aux
- auxiliary_attributes_id   (pk)
- experience_required       (boolean)
- driver_license            (boolean)
- access_to_own_car         (boolean)

dim_job_details
- job_details_id    (pk)
- headline          (varchar)
- description       (varchar)
- employment_type   (varchar)
- duration          (varchar)
- salary_type       (varchar)
- scope_of_work_min (bigint)
- scope_of_work_max (bigint)

PREBUILT MARTS
Use these whenever they satisfy the user's request. They save you from joins.
Must prefix with 'marts.'

mart_summary
- publication_date
- vacancies (You can do like this: SUM(vacancies) AS total_vacancies, but NEVER try to SUM(total_vacancies))
- relevance
- application_deadline
- occupation
- occupation_group
- occupation_field
- employer_name
- employer_workplace
- workplace_municipality
- workplace_region
- experience_required
- driver_license
- access_to_own_car
Good for summary/connections between different columns

mart_top_employers
- employer_name
- workplace_region
- occupation
- total_vacancies  
Good for “top N employers” queries

mart_occupation_group_vacancy_totals
- publication_date
- workplace_region
- workplace_municipality
- occupation_field
- occupation_group
- total_vacancies  
Good for “top N occupation groups” over time or by geography

mart_occupation_vacancy_totals
- publication_date
- occupation
- occupation_group
- occupation_field
- total_vacancies  
Good for “top N occupations” over time

mart_occupation_trends_over_time
- publication_date
- vacancies
- experience_required
- occupation
- occupation_group
- occupation_field  
Good for time-series “trend” plots

JOIN KEYS
- fct_job_ads.employer_id    = dim_employer.employer_id
- fct_job_ads.occupation_id  = dim_occupation.occupation_id
- fct_job_ads.aux_id         = dim_aux.auxiliary_attributes_id
- fct_job_ads.job_details_id = dim_job_details.job_details_id

GENERAL RULES
1. ALWAYS prefix dim tables with `refined.` and marts with `marts.`
2. NEVER reference src_* or int_* models (since they are ephemeral).
3. Prefer a MART if it directly covers the user's ask.
4. When writing ad-hoc SQL, JOIN fact → dim tables using the above keys.
5. Write each query on one line, no Markdown fences.
7. If user is asking for something specific, use aliases to rename columns in the dataframe to increase clarity. For example, if user is asking for total vacancies requiring driver_license=True, use an alias to rename it from "total_vacancies" to "total_vacancies_requiring_driver_license". The same applies to other questions/prompts.
8. Make damned sure that the color arg is an actual column in the dataframe, otherwise the plot will fail.

EXAMPLES
— Top 10 employers for Sjuksköterska —
SELECT employer_name, total_vacancies
FROM refined.mart_top_employers
WHERE occupation = 'Sjuksköterska'
ORDER BY total_vacancies DESC
LIMIT 10

But make your you figure out the valid content of the SQL query
By using an exploratory query to find the right table and columns
"""
