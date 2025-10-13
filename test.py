import json
import os

# Import the specific functions from your new modules
from core_logic.extractor import extract_text_from_pdf
from core_logic.analyzer import analyze_resume_text

# --- Configuration ---
# 🎯 Make sure a resume file exists at this path for testing
TEST_RESUME_PATH = "uploaded_resumes/resume.pdf"

def main():
    """
    A simple script to test the extractor and analyzer modules.
    """
    print("--- 🧪 Starting Test ---")
    
    if not os.path.exists(TEST_RESUME_PATH):
        print(f"🛑 TEST FAILED: The test file was not found at '{TEST_RESUME_PATH}'")
        return

    # --- Step 1: Test the Extractor ---
    print(f"📄 Step 1: Extracting text from '{TEST_RESUME_PATH}'...")
    extracted_text = extract_text_from_pdf(TEST_RESUME_PATH)

    if not extracted_text:
        print("🛑 TEST FAILED: Text extraction returned nothing.")
        return
    
    print("✅ Step 1 complete: Text extracted successfully.")

    # --- Step 2: Test the Analyzer ---
    print("\n🧠 Step 2: Analyzing extracted text with Gemini...")
    analysis_result = analyze_resume_text(extracted_text)

    if not analysis_result:
        print("🛑 TEST FAILED: Analysis returned nothing.")
        return
        
    print("✅ Step 2 complete: Analysis successful.")

    # --- Step 3: Display the Final Result ---
    print("\n--- ✅ Test Passed! Final JSON Output ---")
    # Print the dictionary as a nicely formatted JSON string
    print(json.dumps(analysis_result, indent=4))
    print("-----------------------------------------")


if __name__ == "__main__":
    main()