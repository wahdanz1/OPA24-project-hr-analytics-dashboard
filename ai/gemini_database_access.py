def get_database_instructions() -> str:
    """
    Clear, concise instructions for Gemini on how to query our production
    warehouse. Only the `refined` schema exists at runtime. Use standard SQL.
    """
    return """
AVAILABLE SCHEMAS & TABLES (refined.*)

  • refined.fct_job_ads
      - publication_date (date)
      - job_details_id (pk → dim_job_details.job_details_id)
      - occupation_id  (fk → dim_occupation.occupation_id)
      - employer_id    (fk → dim_employer.employer_id)
      - aux_id         (fk → dim_aux.auxiliary_attributes_id)
      - vacancies, relevance, application_deadline, etc.

  • refined.dim_occupation
      - occupation_id (pk)
      - occupation, occupation_group, occupation_field

  • refined.dim_employer
      - employer_id (pk)
      - employer_name, employer_workplace, workplace_city, workplace_region

  • refined.dim_job_details
      - job_details_id (pk)
      - headline, description, employment_type, duration, etc.

  • refined.dim_aux
      - auxiliary_attributes_id (pk)
      - experience_required, driver_license, access_to_own_car, etc.

JOIN KEYS

  • fct_job_ads.employer_id   = dim_employer.employer_id
  • fct_job_ads.occupation_id = dim_occupation.occupation_id
  • fct_job_ads.job_details_id = dim_job_details.job_details_id
  • fct_job_ads.aux_id         = dim_aux.auxiliary_attributes_id

GENERAL SQL RULES

  1. ALWAYS prefix tables: `refined.fct_job_ads`, `refined.dim_employer`, etc.
  2. NEVER use Jinja or dbt macros: no `{{ ref() }}`, no compile-time helpers.
  3. Write each query on one line. Do NOT wrap in Markdown fences.
  4. Use standard SQL (Postgres / DuckDB dialect). No back-ticks unless required.
  5. When filtering by strings, use case-insensitive comparison:
       WHERE lower(column) = 'value'
     or `ILIKE` if available.

COMMON PATTERNS & EXAMPLES

  • Top N employers for an occupation
    SELECT e.employer_name,
           COUNT(*) AS job_count
    FROM   refined.fct_job_ads f
    JOIN   refined.dim_employer e
      ON   f.employer_id = e.employer_id
    JOIN   refined.dim_occupation o
      ON   f.occupation_id = o.occupation_id
    WHERE  lower(o.occupation) = 'sjukskoterska'
    GROUP BY e.employer_name
    ORDER BY job_count DESC
    LIMIT 10

  • Daily trend of job ads for an occupation
    SELECT f.publication_date,
           COUNT(*) AS job_count
    FROM   refined.fct_job_ads f
    JOIN   refined.dim_occupation o
      ON   f.occupation_id = o.occupation_id
    WHERE  lower(o.occupation) = 'lakare'
    GROUP BY f.publication_date
    ORDER BY f.publication_date

  • Vacancy counts by region
    SELECT d.workplace_region,
           COUNT(*) AS job_count
    FROM   refined.fct_job_ads f
    JOIN   refined.dim_employer d
      ON   f.employer_id = d.employer_id
    GROUP BY d.workplace_region
    ORDER BY job_count DESC

TIPS

  • Use DISTINCT + lower() to discover valid values:
      SELECT DISTINCT lower(occupation) AS candidate
        FROM refined.dim_occupation
       WHERE occupation IS NOT NULL

  • Always JOIN the appropriate dim table before grouping or filtering.

When you include a query in your JSON response, put it under the key
"query" as a plain string. Do NOT include any other keys or commentary.
"""
