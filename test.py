import os
import google.generativeai as genai
from dotenv import load_dotenv

def check_available_models():
    """
    Configures the Gemini API and lists all models that support 'generateContent'.
    """
    # --- 1. Configure and Validate API Key ---
    try:
        load_dotenv()
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found or is empty in your .env file.")
        genai.configure(api_key=api_key)
        print("✅ API Key configured successfully. Fetching available models...\n")
    except Exception as e:
        print(f"🛑 CONFIGURATION FAILED: {e}")
        print("   Please ensure a .env file is in the project's root directory")
        print("   and contains the line: GOOGLE_API_KEY='YourActualKey'")
        return

    # --- 2. List Models that Support the Required Method ---
    print("--- Models that support 'generateContent' ---")
    found_models = False
    for model in genai.list_models():
      # We only want to see models that can actually generate text for our prompts
      if 'generateContent' in model.supported_generation_methods:
        # The model names from the API are 'models/model-name'
        # We'll clean it up to show just 'model-name'
        model_name = model.name.replace("models/", "")
        print(f"✅ {model_name}")
        found_models = True
    
    if not found_models:
        print("No models supporting 'generateContent' were found for this API key.")
    
    print("---------------------------------------------")

if __name__ == "__main__":
    check_available_models()