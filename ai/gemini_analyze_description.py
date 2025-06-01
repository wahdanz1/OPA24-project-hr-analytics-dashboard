import pandas as pd
from .gemini import GeminiHandler

# Function for retrieving the top skills from job descriptions
def get_top_skills(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze job descriptions to extract and count top skills.

    Args:
        dataframe (pd.DataFrame): DataFrame with a 'description' column.

    Returns:
        pd.DataFrame: DataFrame with columns ['description', 'total_occurences'].
    """
    instructions = (
        "You are an HR specialist tasked with analyzing job descriptions. "
        "Your goal is to identify and count the occurrences of skills mentioned in the job descriptions. "
        "Skills can be any word or phrase that indicates a capability or expertise, such as programming languages, tools, or methodologies. "
        "You have been provided with a DataFrame (converted to CSV) containing job descriptions for a specific occupation group and region. "
        "Consider variations of the same skill (e.g., 'kassaarbete' and 'Kassaarbete' should be counted as the same skill)."
        "Format the description with capitalization (e.g., 'Engelska' instead of 'engelska'). "
        "If it is a skill that is something you should have experience of, format it as 'Erfarenhet av [Skill]'. "
        "If it is a skill that is something you should have knowledge of, format it as 'Kunskap om [Skill]'. "
        "If it is a skill that is an educational requirement, format it as 'Utbildad [Skill]', for example 'Tandsköterska' becomes 'Utbildad Tandsköterska'. "
        "Return a DataFrame with two columns, 'description' and 'total_occurences'. "
        "The 'description' column should contain the skill names, and 'total_occurences' should contain the count of each skill. "
        "Rename the column 'description' to 'Skill', and 'total_occurences' to 'Count'. "
        "Sort the dataframe in descending order by 'Count'. "
    )
    return analyze_descriptions(
        dataframe,
        instructions=instructions,
        column_a_name="description",
        column_a_description="Skill extracted from job description",
        column_b_name="total_occurences",
        column_b_description="Count of the occurrences of the skill"
    )

# Function for analyzing job descriptions
def analyze_descriptions(
    dataframe: pd.DataFrame, instructions: str,
    column_a_name: str, column_a_description: str,
    column_b_name: str, column_b_description: str
) -> pd.DataFrame:
    """
    Generic function to analyze a DataFrame using Gemini and return a DataFrame.

    Args:
        dataframe (pd.DataFrame): Input DataFrame.
        instructions (str): Task instructions for Gemini.
        column_a_name (str): Name of the first column in the output.
        column_a_description (str): Description of the first column.
        column_b_name (str): Name of the second column in the output.
        column_b_description (str): Description of the second column.

    Returns:
        pd.DataFrame: Resulting DataFrame as described in the instructions.
    """
    # Initialize Gemini handler
    gemini_handler = GeminiHandler()

    result = gemini_handler.analyze_dataframe(
        dataframe=dataframe,
        instructions=instructions,
        column_a_name=column_a_name,
        column_a_description=column_a_description,
        column_b_name=column_b_name,
        column_b_description=column_b_description
    )

    # Ensure the result is a DataFrame
    if isinstance(result, pd.DataFrame):
        return result
    else:
        # Try to parse result to DataFrame if it's a string (e.g., CSV or JSON)
        try:
            return pd.read_json(result)
        except Exception:
            try:
                return pd.read_csv(result)
            except Exception:
                raise ValueError("Gemini did not return a valid DataFrame or parseable string.")