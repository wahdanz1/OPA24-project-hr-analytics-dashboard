def get_tool_instructions() -> str:
    """
    Plot helpers + a strict “pick table → run query → plot” protocol.
    Gemini must never invent fields or tables.
    """
    return """
NO GUESSING OF FIELDS OR TABLES
• You may ONLY query tables & columns listed in get_database_instructions().
• If the mart for the ask exists → use it.
• Otherwise → JOIN fact + dim by keys exactly.

PLOT HELPERS (only in final step)
def create_vertical_bar_chart(data, **kwargs): ...
def create_line_chart(data, **kwargs): ...

FULL QUERY PROTOCOL
STEP 0 • Identify intent
  • “top N X by Y” → use mart_top_* if X=employers/occupations
  • “trend” → use mart_occupation_trends_over_time
  • Otherwise → ad-hoc join between fact & relevant dim

STEP 1 • Build SQL
  • MART version:
      SELECT * FROM refined.mart_<appropriate> 
      WHERE <filters> 
      ORDER BY <metric> DESC 
      LIMIT N
  • AD-HOC version:
      SELECT d.<field> AS category, AGG(f.<metric>) AS value
      FROM refined.fct_job_ads f
      JOIN refined.dim_<X> d ON f.<fk> = d.<pk> (X = occupation OR employer OR job_details OR aux, and fk = X_id (unless dim_aux, then it's auxillary_attributes_id))
      WHERE lower(d.<field>) = '<value>'
      GROUP BY d.<field>
      ORDER BY value DESC
      LIMIT N

STEP 2 • Output JSON
{
  "response": "<short human summary>",
  "query": "<the one-line SQL>",
  "methods": [
    {
      "name": "<choose appropriate create_*_chart>",
      "args": {
        "data": "__query_result__",
        "x_value": "<x column>",
        "y_value": "<y column>",
        "title": "<chart title>"
        "color_column": "<one of the columns in the dataframe>"
        "x_label": "<x-axis label>",
        "y_label": "<y-axis label>"
      }
}



HARD RULES
• Only one SQL in "query" per JSON.   s
• Only chart helpers in "methods".  
• Never wrap JSON in fences.  
• NEVER invent tables or columns.
  NEVER INVENT TABLES OR COLUMNS.
    NEVER INVENT TABLES OR COLUMNS.
    NEVER INVENT TABLES OR COLUMNS.
"""
