# OPA24: Project - HR Analytics Proof of Concept
This is the final group project of the course OPA24 (Object-oriented Programming with AI). Below you can find the project description with details about the assignment.

## Project Description
<details>
<summary>Details about the project - click to expand/collapse</summary>

### Purpose
The project aims to implement the modern data stack to solve a real-world problem. In addition to using a certain number of techniques, there is a focus on working together in a data team. This includes both agile development and being able to use Git and GitHub in a team

### Scenario
Imagine you are a data engineer for a HR agency. Here's an overview of the business model of this agency:


Talent acquisition specialists work with different occupation fields. According to the opening job ads on Arbetsförmedlingen, they will:
- search and contact potential candidates from LinkedIn
- contact and market those potential candidates to corresponding employers

Therefore, they constantly analyze job ads in order to understand which types of candidates they should approach. Currently, every begining of the week, they manually browse the homepage of Arbetsförmedlingen and download a list of opening job ads to guide their work over the week. However, they are not able to draw insights from these job ads as:
- the information is messy
- they have spent too much time to manually collect and clean data so that they do not have much time to analyze the data, which is important to improve the efficiency of their work


Now, you are given a task to create a data pipeline for the team of talent acquisition specialists to:
- automate the data extraction from Jobtech API of Arbetsförmedlingen
- transform and structure data according to a dimensional model
- design a dashboard for talent acquisition specialists to analyse numbers of vacancies by city, by occupation and by employment types etc, for each of the occupation fields
</details>

<br>

## How to run
1. **Clone the repository:**
    ```git bash
    git clone https://github.com/wahdanz1/OPA24-project-hr-analytics-dashboard
2. **Navigate to the project root:**
    ```git bash
    cd OPA24-project-hr-analytics-dashboard
3. **Create virtual environment (with `uv venv`):**
    ```git bash
    uv venv .venv
4. **Activate virtual environment:**
    ```git bash
    .venv\scripts\activate (Windows)
    OR
    source source .venv/bin/activate (MacOS/Linux)
5. **Install dependencies from the `requirements.lock`-file:**
    ```git bash
    uv pip install -r requirements.lock.txt
6. **Run the `first_time_run.py`-script in the `scripts/` directory**
    > ⚠️ Do note that this process might take some time - the first pipeline-run will fetch data from 2 months back up until present day, followed by generate dbt docs.
7. **Run the Streamlit Dashboard with the following command (from project root):**
    ```git bash
    streamlit run app.py
<br>

## Profiles.yml:
```yml
job_market:
  outputs:
    dev:
      type: duckdb
      path: job_ads.duckdb
      threads: 1

  target: dev
```

<br>

## Documentation (dbt docs)
Documentation can be accessed through the dashboard (**dbt docs**), but if you want to generate it locally for use with `dbt docs serve`, you can run the script `generate_and_deploy_docs.py` (in the project root).

<a href="https://wahdanz1.github.io/OPA24-project-hr-analytics-dashboard/" target="_blank">
  <img src="https://img.shields.io/badge/📘%20View%20DBT%20Documentation-blue?style=for-the-badge" alt="DBT Docs">
</a>

<br>

## Tests
The project includes a series of **dbt tests** to ensure data quality and trustworthiness. These are defined in the `/tests` directory and are automatically executed when running `dbt test`. Here's a brief overview of the tests:

- **`test_duplicate_primary_keys`**  
  Ensures no duplicate primary keys exist in key models, which could compromise downstream joins and analysis.

- **`test_employer_org_number`**  
  Validates that all employer organization numbers are exactly 10 digits, as expected by Swedish org number standards.

- **`test_future_publication_date`**  
  Checks for any job ads with a publication date set in the future, which could indicate incorrect or dirty data.

- **`test_missing_employer_name`**  
  Flags records where `employer_name` is missing or null — important for attribution and insights.

- **`test_missing_occupation_id`**  
  Detects rows with missing occupation identifiers, which are necessary for classification and analysis.

You can run all tests with:

```bash
cd job_market
dbt test
```
More details and test results can be found in the <a href="https://wahdanz1.github.io/OPA24-project-hr-analytics-dashboard/" target="_blank">DBT Documentation</a>.

<br>

## Credits
<a href="https://github.com/wahdanz1" target="_blank">`wahdanz1`</a>

<a href="https://github.com/Remmold" target="_blank">`Remmold`</a>

<a href="https://github.com/Oskara1209" target="_blank">`Oskara1209`</a>