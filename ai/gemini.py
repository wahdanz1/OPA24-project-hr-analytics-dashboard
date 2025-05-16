from dotenv import load_dotenv
import os
import google.genai as genai    
from pathlib import Path
# gemini_handler = GeminiHandler()
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
    def get_response(self,prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response



