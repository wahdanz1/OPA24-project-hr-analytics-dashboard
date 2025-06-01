from dotenv import load_dotenv
from .gemini_database_access import get_database_instructions
from .gemini_tool_instructions import get_tool_instructions
from .gemini_personality import get_statistical_consultant_personality
from .gemini_response_format import get_response_format
import os
import google.genai as genai    
from pathlib import Path
import json
import pandas as pd

class GeminiHandler:

    def __init__(self):
        self.client = self.get_gemini_client()
        self.model = "gemini-2.0-flash"

    # Get the Gemini client
    def get_gemini_client(self):
        working_directory = Path(__file__).resolve().parent.parent
        load_dotenv(working_directory / ".env")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=gemini_api_key)
        return client
    
    # Get the response from the Gemini model
    def get_response(self, prompt, history=None, csv_string=None):
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"""
            database instructions: {get_database_instructions()}
            this is the tool instructions: {get_tool_instructions()}
            this is the personality prompt: {get_statistical_consultant_personality()}
            this is the user prompt: {prompt}
            this is the response format: {get_response_format()}
            this is the history of the conversation: {history}
            if there is a csv file, please use it to answer the question: {csv_string if csv_string else "No CSV file provided"}

            Please provide a JSON response with the required keys as specified in the response format.
            Do not include any Markdown fences or additional commentary outside the JSON object.
            """
        )

        raw_text = response.candidates[0].content.parts[0].text
        if raw_text.startswith("```json"):
            raw_text = raw_text.strip("```json").strip("```").strip()

        try:
            # Try parsing the string as JSON
            parsed = json.loads(raw_text)
            return parsed
        except json.JSONDecodeError as e:
            # Return fallback response with error info
            return {
                "response": "There was an error parsing the response.",
                "error": str(e),
                "raw": raw_text
            }

    # Generate response (lite)
    def get_response_lite(self, prompt, csv_string):
        response = self.client.models.generate_content(
            model = self.model,
            contents = f"""
                        Instructions: {prompt}\n
                        DataFrame, converted to CSV: {csv_string}\n
                        Please provide a JSON response with the required keys as specified in the response format.
                        Do not include any Markdown fences or additional commentary outside the JSON object.
                        """,
        )

        raw_text = response.candidates[0].content.parts[0].text
        if raw_text.startswith("```json"):
            raw_text = raw_text.strip("```json").strip("```").strip()

        try:
            # Try parsing the string as JSON
            parsed = json.loads(raw_text)
            return parsed
        except json.JSONDecodeError as e:
            # Return fallback response with error info
            return {
                "response": "There was an error parsing the response.",
                "error": str(e),
                "raw": raw_text
            }

    def analyze_dataframe(self, dataframe, instructions, column_a_name, column_a_description, column_b_name, column_b_description):
        # Convert DataFrame to CSV string
        csv_string = dataframe.to_csv(index=False)

        # Build a detailed prompt for Gemini
        prompt = (
            f"{instructions}\n"
            f"Column 1: {column_a_name} - {column_a_description}\n"
            f"Column 2: {column_b_name} - {column_b_description}\n"
            f"Analyze the provided CSV data and return a JSON array of objects with keys '{column_a_name}' and '{column_b_name}'."
        )

        # Call Gemini
        response = self.get_response_lite(prompt, csv_string=csv_string)

        # Expecting a JSON array in response
        if isinstance(response, dict) and "error" in response:
            raise ValueError(f"Gemini error: {response['error']}\nRaw: {response.get('raw', '')}")

        # If Gemini returns a list of dicts, convert to DataFrame
        if isinstance(response, list):
            return pd.DataFrame(response)

        # If Gemini returns a dict with a key containing the data
        if isinstance(response, dict):
            # Try to find a key with a list value
            for v in response.values():
                if isinstance(v, list):
                    return pd.DataFrame(v)
            # Or if the dict itself is the data
            return pd.DataFrame([response])

        # If Gemini returns a string, try to parse as JSON or CSV
        if isinstance(response, str):
            try:
                return pd.read_json(response)
            except Exception:
                try:
                    return pd.read_csv(pd.compat.StringIO(response))
                except Exception:
                    raise ValueError("Gemini did not return a valid DataFrame or parseable string.")

        raise ValueError("Gemini did not return a valid DataFrame or parseable string.")
