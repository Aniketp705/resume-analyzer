import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# --- Internal CSS Styling ---
# All the CSS is now inside this multi-line string
page_style = """
    /* --- Import a modern font --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* --- Animated Gradient Background (Idle Animation) --- */
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    body {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(-45deg, #1a202c, #2d3748, #4a5568, #2d3748);
        background-size: 400% 400%;
        animation: gradient-animation 15s ease infinite;
    }
    
    /* --- Main App Container with Glassmorphism Effect --- */
    .main-container {
        background-color: rgba(26, 32, 44, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.5rem;
    }

    /* Hide Streamlit's default elements for a cleaner look */
    header, footer { visibility: hidden; }

    /* --- Fade-in Animation for Elements --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    h1, .stMarkdown {
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    /* --- Styled, Hoverable Button --- */
    div[data-testid="stButton"] > button {
        background: linear-gradient(45deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* --- Results Display: The Profile Card --- */
    .results-container {
        animation: fadeIn 1s ease-out 0.5s forwards;
        opacity: 0; /* Start hidden for animation */
        margin-top: 2rem;
    }
    .candidate-header h2 { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.2rem; color: #ffffff; }
    .candidate-header p { font-size: 1rem; color: #a0aec0; margin: 0; }
    .summary-text { color: #cbd5e0; font-size: 1.05rem; margin-top: 1.5rem; }
    
    /* --- Skill Tags with Hover Animation --- */
    .skills-container { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1rem; }
    .skill-tag {
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 0.4rem 1rem;
        border-radius: 16px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: transform 0.2s ease, background-color 0.2s ease;
    }
    .skill-tag:hover { transform: scale(1.08); background-color: #4a5568; }
    
    /* --- Work/Education History Items --- */
    .history-item { padding: 1.5rem 0; border-bottom: 1px solid #2d3748; }
    .history-item:last-child { border-bottom: none; }
    .job-title { font-size: 1.2rem; font-weight: 600; color: #ffffff; margin: 0; }
    .company-info { font-size: 1rem; color: #a0aec0; margin: 0.2rem 0 0.8rem 0; }
    .responsibilities ul { margin: 0; padding-left: 1.2rem; color: #cbd5e0; }
"""

# Inject the CSS into the app
st.markdown(f'<style>{page_style}</style>', unsafe_allow_html=True)

# Wrap the main content in a div for the glassmorphism effect
# st.markdown('<div class="main-container">', unsafe_allow_html=True)

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
                    result = response.json()
                    
                    # --- Profile Card Display Logic ---
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    personal = result.get('personal_details', {})
                    st.markdown(f"""
                        <div class="candidate-header">
                            <h2>{personal.get('name', 'Name not found')}</h2>
                            <p>📧 {personal.get('email', 'N/A')} | 📞 {personal.get('phone_number', 'N/A')} | 📍 {personal.get('location', 'N/A')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.divider()
                    st.subheader("📌 Professional Summary")
                    st.markdown(f"<p class='summary-text'>{result.get('professional_summary', 'Not found.')}</p>", unsafe_allow_html=True)
                    st.subheader("🛠️ Skills")
                    skills = result.get('skills', [])
                    if skills:
                        skill_tags = "".join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
                        st.markdown(f'<div class="skills-container">{skill_tags}</div>', unsafe_allow_html=True)
                    st.subheader("💼 Work Experience")
                    work_experience = result.get('work_experience', [])
                    if work_experience:
                        for job in work_experience:
                            st.markdown(f"""
                                <div class="history-item">
                                    <p class="job-title">{job.get('job_title', 'N/A')}</p>
                                    <p class="company-info">{job.get('company', 'N/A')} | {job.get('duration', 'N/A')}</p>
                                    <div class="responsibilities">
                                        <ul>{''.join([f"<li>{resp}</li>" for resp in job.get('responsibilities', [])])}</ul>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    st.subheader("🎓 Education")
                    education = result.get('education', [])
                    if education:
                        for edu in education:
                            st.markdown(f"""
                                <div class="history-item">
                                    <p class="job-title">{edu.get('degree', 'N/A')}</p>
                                    <p class="company-info">{edu.get('institution', 'N/A')} ({edu.get('graduation_year', 'N/A')})</p>
                                </div>
                            """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error(f"API Error: {response.json().get('error', 'An unknown error occurred.')}")
            except requests.exceptions.RequestException:
                st.error("Connection Error: Could not connect to the backend.")
