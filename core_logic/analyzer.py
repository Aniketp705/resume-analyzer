import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def extract_resume_data(resume_text: str) -> dict | None:
    """
    Uses the FAST 'gemini-flash-latest' model for simple data extraction.
    """
    try:
        load_dotenv()
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found or is empty in your .env file.")
        genai.configure(api_key=api_key) # type: ignore
    except Exception as e:
        print(f"🛑 CONFIGURATION ERROR: {e}")
        return None

    generation_config = genai.GenerationConfig(response_mime_type="application/json")
    # Use the latest, fastest Flash model for this task
    model = genai.GenerativeModel('gemini-flash-latest', generation_config=generation_config)
    
    # A simple, direct prompt is more efficient for the Flash model
    prompt = f"""
    You are an expert resume parser. Extract the content from the following resume text.
    
    Return a JSON object with the following exact keys: 
    "personal_details", "professional_summary", "skills", "work_experience", and "education".

    If a value for any field is not found, use `null`. For lists, use an empty list `[]`.

    Resume Text:
    ---
    {resume_text}
    ---
    """
    
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"🛑 An unexpected error occurred during extraction: {e}")
        return None

