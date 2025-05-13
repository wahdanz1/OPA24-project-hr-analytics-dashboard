# OPA24: Project - HR Analytics Proof of Concept
This is the final group project of the course OPA24 (Object-oriented Programming with AI). Below is the project description:
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

## How to run
1. **Clone the repository:**
    ```git bash
    git clone https://github.com/wahdanz1/OPA24-project-hr-analytics-dashboard
2. **Navigate to the project root:**
    ```git bash
    cd OPA24-project-hr-analytics-dashboard
3. **Create virtual environment (with ```uv venv```):**
    ```git bash
    uv venv .venv
4. **Activate virtual environment:**
    ```git bash
    .venv\scripts\activate (Windows)
    OR
    source source .venv/bin/activate (MacOS/Linux)
5. **Install dependencies from the ```requirements.lock```-file:**
    ```git bash
    uv pip install -r requirements.lock.txt
6. **Run the script in the project root called ```first_time_run.py```**
    > ⚠️ Do note that this process might take some time - the first pipeline-run will fetch data from 6 months back up until present day.
7. **Run the Streamlit Dashboard with the following command (from project root):**
    ```git bash
    streamlit run app.py
8. **Use the buttons in the sidebar to navigate the dashboard!**