from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(prompt):
    short_prompt = f"Answer in 3-4 sentences only: {prompt}"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=short_prompt
        )
        
        return response.text
    except Exception as e:
        return f"Error: {e}"