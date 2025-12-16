import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

def get_resume_feedback(extracted_data: dict, target_job_profile: str) -> dict | None:
    """
    Uses 'gemini-1.5-flash' for deep analysis.
    Includes retry logic and forced env reloading.
    """
    try:
        # override=True ensures we read the NEW key if you changed the .env file
        load_dotenv(override=True) 
        api_key = os.environ.get("GOOGLE_API_KEY")
        
        if not api_key:
            print("🛑 ERROR: GOOGLE_API_KEY not found.")
            return None
            
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"🛑 CONFIGURATION ERROR: {e}")
        return None

    generation_config = genai.GenerationConfig(response_mime_type="application/json")
    model = genai.GenerativeModel('gemini-2.5-flash', generation_config=generation_config)
    
    resume_json_string = json.dumps(extracted_data, indent=2)

    prompt = f"""
    You are an expert career coach. Analyze the candidate's extracted resume data, provided as a JSON object,
    in the context of the target job profile: '{target_job_profile}'.

    Return a concise, actionable JSON object with the following exact structure:
    {{
      "resume_score": <An integer score from 0-100>,
      "main_feedback": "<A single, concise sentence summarizing the most important area for improvement.>",
      "strengths": ["<A list of 2-3 key strengths of the resume.>"],
      "top_3_improvements": [
        {{
          "area": "Professional Summary",
          "suggestion": "<A brief, actionable suggestion for the summary.>",
          "example_rewrite": "<A rewritten, impactful professional summary tailored for the role.>"
        }},
        {{
          "area": "Action Verbs / Keywords",
          "suggestion": "<Explain why stronger verbs are needed.>",
          "examples": {{"weak_verbs": ["<List of 2-3 weak verbs>"], "stronger_verbs": ["<List of 2-3 better alternatives>"]}}
        }},
        {{
          "area": "Missing Keywords",
          "suggestion": "<Explain why adding specific keywords is important for ATS.>",
          "keywords_to_add": ["<A short list of 3-5 of the MOST CRITICAL missing keywords>"]
        }}
      ]
    }}

    Candidate's Extracted Resume Data:
    ---
    {resume_json_string}
    ---
    """
    
    # Retry logic for handling 429 errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Quota exceeded. Retrying in {2 * (attempt + 1)} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(2 * (attempt + 1)) # Exponential backoff: 2s, 4s, 6s
            else:
                print(f"🛑 An unexpected error occurred during feedback generation: {e}")
                return None
    
    print("🛑 Failed to get feedback after multiple retries.")
    return None


def get_career_roadmap(extracted_data: dict, target_job_profile: str) -> list | None:
    """
    Uses Gemini Flash to generate a JSON-based career roadmap.
    Includes retry logic and forced env reloading.
    """
    try:
        load_dotenv(override=True)
        api_key = os.environ.get("GOOGLE_API_KEY")
        
        if not api_key:
            print("🛑 ERROR: GOOGLE_API_KEY not found.")
            return None
            
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"🛑 CONFIGURATION ERROR: {e}")
        return None
    
    generation_config = genai.GenerationConfig(response_mime_type="application/json")
    model = genai.GenerativeModel('gemini-2.5-flash', generation_config=generation_config)
    
    current_skills = extracted_data.get('skills', [])

    prompt = f"""
    You are an expert career coach. Analyze the user's current skills and their target job role.
    Your task is to generate a step-by-step career roadmap as a JSON array.

    The user's target job is: '{target_job_profile}'
    The user's current skills are: {current_skills}

    The JSON array must be a list of "phase" objects. Each object must have:
    1.  `phase`: An integer (1, 2, 3...).
    2.  `title`: A short title for the phase (e.g., "Core ML Engineering").
    3.  `summary`: A one-sentence summary of this phase.
    4.  `steps`: An array of objects, each with:
        * `name`: The name of the skill or topic (e.g., "Docker").
        * `status`: A string. It MUST be "completed" if the skill is in the user's current skill list. It MUST be "in_progress" or "to_learn" if it's not.

    Carefully compare the user's current skills with the skills needed for the target job to decide the status for each step.
    Create 3-5 logical phases, starting from their current skills and ending at their target job.
    """
    
    # Retry logic for handling 429 errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Quota exceeded. Retrying in {2 * (attempt + 1)} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(2 * (attempt + 1))
            else:
                print(f"🛑 An unexpected error occurred during roadmap generation: {e}")
                return None

    print("🛑 Failed to get roadmap after multiple retries.")
    return None