# check_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load and configure your API key
load_dotenv()
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API Key not found in .env file.")
    genai.configure(api_key=api_key)
    print("✅ API Key configured. Fetching available models...\n")
except Exception as e:
    print(f"🛑 Configuration failed: {e}")
    exit()

# List all available models and check their capabilities
print("--- Models that support 'generateContent' ---")
for model in genai.list_models():
  if 'generateContent' in model.supported_generation_methods:
    # The model names are in the format 'models/model-name'
    # We only need the 'model-name' part
    model_name = model.name.replace("models/", "")
    print(f"✅ {model_name}")
print("---------------------------------------------")