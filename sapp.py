import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# --- Function to load and inject CSS ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply the custom CSS
load_css("static/style.css")

# --- App UI ---
st.title("📄 AI Resume Analyzer")
st.markdown("Upload a PDF resume to instantly extract key information and insights.")

FLASK_API_URL = "http://127.0.0.1:5001/analyze"

uploaded_file = st.file_uploader(
    "Choose a resume PDF to analyze",
    type="pdf",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    if st.button("Analyze Resume"):
        with st.spinner("Our AI is analyzing the document... Please wait."):
            try:
                files = {'resume': (uploaded_file.name, uploaded_file, 'application/pdf')}
                response = requests.post(FLASK_API_URL, files=files)
                
                if response.status_code == 200:
                    st.success("Analysis Complete!")
                    analysis_result = response.json()
                    
                    # --- Display results in a more structured way ---
                    st.subheader("Extracted Information")
                    
                    personal = analysis_result.get('personal_details', {})
                    skills = analysis_result.get('skills', [])
                    summary = analysis_result.get('professional_summary', "Not found.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input("Name", personal.get('name'), disabled=True)
                        st.text_input("Email", personal.get('email'), disabled=True)
                        st.text_input("Location", personal.get('location'), disabled=True)
                    with col2:
                        st.text_input("Phone", personal.get('phone_number'), disabled=True)
                        st.text_area("Skills", ", ".join(skills) if skills else "Not found.", height=125, disabled=True)

                    st.text_area("Professional Summary", summary, height=150, disabled=True)
                    st.divider()
                    st.subheader("Raw JSON Output")
                    st.json(analysis_result)
                else:
                    error_data = response.json()
                    st.error(f"API Error: {error_data.get('error', 'An unknown error occurred.')}")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: Could not connect to the backend. Is the Flask server running?")