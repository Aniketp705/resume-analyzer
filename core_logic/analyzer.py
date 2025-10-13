import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def analyze_resume_text(resume_text: str) -> dict | None:
    try:
        load_dotenv()
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found or is empty in your .env file.")
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"🛑 CONFIGURATION ERROR: {e}")
        return None

    # --- 2. Call the Gemini API ---
    try:
        generation_config = genai.GenerationConfig(response_mime_type="application/json")
        model = genai.GenerativeModel('gemini-pro-latest', generation_config=generation_config)
        
        # 🎯 THE NEW, DETAILED PROMPT FOR OPTIMAL EXTRACTION
        prompt = f"""
          You are an expert HR data extraction system. Your task is to meticulously parse the provided resume text and return a structured JSON object. Follow the examples provided to understand the exact format and level of detail required.

          ---
          **EXAMPLE 1**

          **Resume Text:**
          "John Doe, a senior software developer with 8 years of experience. Contact: j.doe@email.com. Lives in San Francisco, CA. Expert in Python and Java. Previously worked at TechCorp."

          **JSON Output:**
          {{
            "personal_details": {{ "name": "John Doe", "email": "j.doe@email.com", "phone_number": null, "location": "San Francisco, CA" }},
            "professional_summary": "A senior software developer with 8 years of experience, specializing in Python and Java.",
            "total_experience_years": 8,
            "skills": ["Python", "Java"],
            "work_experience": [{{ "job_title": "Senior Software Developer", "company": "TechCorp", "duration": null, "responsibilities": [] }}],
            "education": []
          }}
          ---
          **EXAMPLE 2**

          **Resume Text:**
          "Jane Smith | Data Analyst | jane@web.com | Boston, MA. Skilled in SQL and Tableau. Graduated from Boston University in 2022 with a B.S. in Analytics."

          **JSON Output:**
          {{
            "personal_details": {{ "name": "Jane Smith", "email": "jane@web.com", "phone_number": null, "location": "Boston, MA" }},
            "professional_summary": "A data analyst skilled in SQL and Tableau.",
            "total_experience_years": 2,
            "skills": ["SQL", "Tableau"],
            "work_experience": [],
            "education": [{{ "degree": "B.S. in Analytics", "institution": "Boston University", "graduation_year": 2022 }}]
          }}
          ---

          Now, analyze the following resume text based on these examples. If a value for any field is not found, use `null`. For lists, use an empty list `[]`.

          **Resume Text to analyze:**
          ---
          {resume_text}
          ---
          ...
          **RULES TO FOLLOW:**
          1.  **Do Not Hallucinate:** If information is not present in the resume text, you MUST use `null` or `[]`. Do not invent or infer data.
          2.  **Be Concise:** Keep summaries and responsibility descriptions brief and to the point.
          3.  **Calculate Experience:** For `total_experience_years`, estimate the total years based on the dates provided in the work history. If no dates are present, make a reasonable estimation from the text.
          4.  **Extract Skills Verbatim:** Extract skills as they are written in the resume. Do not add skills that are not explicitly mentioned.
          ...
          """
        
        response = model.generate_content(prompt)
        return json.loads(response.text)
        
    except Exception as e:
        print(f"🛑 An unexpected error occurred during the API call: {e}")
        return None