from dotenv import load_dotenv
from gemini_database_access import get_database_instructions
from gemini_tool_instructions import get_tool_instructions
from gemini_personality import get_statistical_consultant_personality
from gemini_response_format import get_response_format
import os
import google.genai as genai    
from pathlib import Path
import json

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

    def get_response(self, prompt, history=None,csv_string=None):
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





