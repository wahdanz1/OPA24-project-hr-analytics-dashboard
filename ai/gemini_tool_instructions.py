def get_tool_instructions() -> str:
    """
    Plot helpers plus a strict fetch-all → choose-best → plot protocol.
    Gemini must scan the database for actual values, pick the best match
    by similarity + demand, then run analysis and plot. No hard-coded maps.
    """
    return """
Absolute no-guess rule:
If you have not verified a value via DISTINCT, keep iterating Step 1 or ask the user. Never guess.

Plot helpers (only in Step 4):
def create_horizontal_bar_chart(data, **kwargs): ...
def create_vertical_bar_chart(data, **kwargs): ...
def create_line_chart(data, **kwargs): ...

Full protocol (MANDATORY)

STEP 1 - Fetch all candidates (case-insensitive)
SQL:
SELECT DISTINCT lower({field}) AS candidate
FROM   {dimension_table}
WHERE  {field} IS NOT NULL
Put this SQL in "query", set methods=null, stop=false,
prompt_to_self="STEP2"

STEP 2 - Pick top 3 by similarity
After you have the candidate list, compute similarity to user input for each:
• exact substring → +2
• Levenshtein ≤ 3  → +1
• otherwise        → 0
Select the 3 candidates with highest scores. Then for each of those, run:
SELECT '{c}' AS candidate, COUNT(*) AS row_cnt
FROM   refined.fct_job_ads f
JOIN   {dimension_table} d ON f.{fk}=d.{pk}
WHERE  lower(d.{field}) = '{c}'
JSON each turn: query=<SQL>, methods=null, stop=false,
prompt_to_self="STEP2"

STEP 3 - Choose best candidate
When you have three {candidate,row_cnt} results:
- Discard any with row_cnt = 0
- Pick the one with highest similarity + non-zero row_cnt
- If none remain: ask the user and set stop=true
- Otherwise: record chosen and proceed

Output JSON:
{
  "response": "Best candidate is {chosen}.",
  "candidates": [ ...list of three objects... ],
  "chosen": "{chosen}",
  "query": null,
  "methods": null,
  "prompt_to_self": "STEP4",
  "stop": false
}

STEP 4 - Analysis & Plot
First, run analysis SQL (case-insensitive):
SELECT e.employer_name, COUNT(*) AS job_count
FROM   refined.fct_job_ads f
JOIN   refined.dim_employer e ON f.employer_id=e.employer_id
JOIN   refined.dim_occupation o ON f.occupation_id=o.occupation_id
WHERE  lower(o.occupation) = '{chosen}'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
JSON: query=<SQL>, methods=null, stop=false, prompt_to_self="PLOT"

Then final JSON:
{
  "response": "Here are the top employers for {chosen}.",
  "query": null,
  "methods": [
    {
      "name": "create_horizontal_bar_chart",
      "args": {
        "data": "__query_result__",
        "x_value": "job_count",
        "y_value": "employer_name",
        "title": "Top employers for {chosen}"
      }
    }
  ],
  "prompt_to_self": null,
  "stop": true
}

Hard rules:
- Steps 1–3: methods must be null.
- Step 4: methods may only contain create_horizontal_bar_chart,
  create_vertical_bar_chart, or create_line_chart.
- Never guess unchecked values.
- Never plot an empty DataFrame.
- Never wrap JSON in markdown fences.
"""
