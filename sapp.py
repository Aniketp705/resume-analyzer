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
page_style = """
    /* --- Import a modern font --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* --- Animated Gradient Background --- */
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
    
    /* --- Main App Container --- */
    .main-container {
        background-color: rgba(26, 32, 44, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.5rem;
    }

    /* Hide Streamlit's default elements */
    header, footer { visibility: hidden; }

    /* --- Animations and Buttons --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    h1, .stMarkdown { animation: fadeIn 0.8s ease-out forwards; }
    div[data-testid="stButton"] > button {
        background: linear-gradient(45deg, #6366f1, #8b5cf6);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
    }
    
    /* --- Profile Card Styles --- */
    .results-container { animation: fadeIn 1s ease-out 0.5s forwards; opacity: 0; margin-top: 2rem; }
    .candidate-header h2 { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.2rem; color: #ffffff; }
    .candidate-header p { font-size: 1rem; color: #a0aec0; margin: 0; }
    .summary-text { color: #cbd5e0; font-size: 1.05rem; margin-top: 1.5rem; }
    .skills-container { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1rem; }
    .skill-tag {
        background-color: #2d3748; color: #e2e8f0; padding: 0.4rem 1rem; border-radius: 16px;
        font-size: 0.9rem; font-weight: 500; transition: transform 0.2s ease, background-color 0.2s ease;
    }
    .skill-tag:hover { transform: scale(1.08); background-color: #4a5568; }
    .history-item { padding: 1.5rem 0; border-bottom: 1px solid #2d3748; }
    .history-item:last-child { border-bottom: none; }
    .job-title { font-size: 1.2rem; font-weight: 600; color: #ffffff; margin: 0; }
    .company-info { font-size: 1rem; color: #a0aec0; margin: 0.2rem 0 0.8rem 0; }
    .responsibilities ul { margin: 0; padding-left: 1.2rem; color: #cbd5e0; }
    
    /* --- File Uploader --- */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #4a5568;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1.5rem; border-radius: 12px;
    }
    
    /* --- NEW ROADMAP STYLES --- */
    .roadmap-phase {
        background-color: rgba(26, 32, 44, 0.7); /* A slightly darker card */
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 1s ease-out;
    }
    .roadmap-phase h3 { /* Phase Title */
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-top: 0;
    }
    .roadmap-phase p { /* Phase Summary */
        font-size: 1rem;
        color: #a0aec0;
        margin-bottom: 1.5rem;
    }
    .roadmap-steps-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
    }
    .step-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 1rem;
        border-radius: 16px;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid;
    }
    .status-completed {
        background-color: rgba(56, 161, 105, 0.1);
        color: #68d391;
        border-color: #38a169;
    }
    .status-in_progress {
        background-color: rgba(221, 107, 32, 0.1);
        color: #f6ad55;
        border-color: #dd6b20;
    }
    .status-to_learn {
        background-color: #2d3748;
        color: #a0aec0;
        border-color: #4a5568;
    }
"""
st.markdown(f'<style>{page_style}</style>', unsafe_allow_html=True)

# --- API Endpoints ---
FLASK_ANALYZE_URL = "http://127.0.0.1:5001/analyze"
FLASK_SUGGEST_URL = "http://127.0.0.1:5001/suggest-improvements"
FLASK_ROADMAP_URL = "http://127.0.0.1:5001/generate-roadmap" # New Endpoint

# --- Session State Initialization ---
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'suggestions_data' not in st.session_state:
    st.session_state.suggestions_data = None
if 'roadmap_data' not in st.session_state:
    st.session_state.roadmap_data = None

# # --- Main App Container ---
# st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("📄 AI Resume Analyzer, Improver & Roadmap Generator")
st.markdown("Upload a resume, get suggestions, and generate a career roadmap.")

# --- Step 1: File Upload (Fast Extraction) ---
uploaded_file = st.file_uploader(
    "Step 1: Upload your resume PDF for analysis.",
    type="pdf",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Use the file uploader's built-in button as the trigger
    with st.spinner("Analyzing (Fast)... Please wait."):
        try:
            files = {'resume': (uploaded_file.name, uploaded_file, 'application/pdf')}
            response = requests.post(FLASK_ANALYZE_URL, files=files)
            
            if response.status_code == 200:
                st.success("Analysis Complete!")
                st.session_state.extracted_data = response.json()
                st.session_state.suggestions_data = None # Clear old suggestions
                st.session_state.roadmap_data = None # Clear old roadmap
            else:
                st.session_state.extracted_data = None
                st.error(f"API Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.RequestException:
            st.session_state.extracted_data = None
            st.error("Connection Error: Could not connect to the backend.")

# --- Display Extracted Data ---
if st.session_state.extracted_data:
    result = st.session_state.extracted_data
    with st.expander("Show Extracted Resume Data", expanded=False):
        st.markdown('<div class="results-container" style="opacity: 1;">', unsafe_allow_html=True)
        personal = result.get('personal_details', {})
        st.markdown(f"""
            <div class="candidate-header">
                <h2>{personal.get('name', 'Name not found')}</h2>
                <p>📧 {personal.get('email', 'N/A')} | 📞 {personal.get('phone_number', 'N/A')} | 📍 {personal.get('location', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)
        # ... (rest of your profile card display logic) ...
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- Step 2 & 3: Improver and Roadmap ---
    st.markdown("<h2>Step 2 & 3: Get AI-Powered Feedback</h2>", unsafe_allow_html=True)
    target_job = st.text_input(
        "Enter your target job profile:",
        placeholder="e.g., Machine Learning Engineer",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    
    with col1:
        # --- Step 2: Get Suggestions ---
        if st.button("Get Improvement Suggestions (Pro)", key="btn_get_suggestions", use_container_width=True):
            if not target_job.strip():
                st.error("Please enter a target job profile.")
            else:
                with st.spinner("Our AI Coach is thinking... Please wait."):
                    payload = {"extracted_data": st.session_state.extracted_data, "target_job": target_job}
                    response = requests.post(FLASK_SUGGEST_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state.suggestions_data = response.json()
                    else:
                        st.error(f"API Error: {response.json().get('error', 'Unknown error')}")

    with col2:
        # --- Step 3: Get Roadmap ---
        if st.button("Generate Career Roadmap (Pro)", key="btn_get_roadmap", use_container_width=True):
            if not target_job.strip():
                st.error("Please enter a target job profile.")
            else:
                with st.spinner("Generating your personalized roadmap..."):
                    payload = {"extracted_data": st.session_state.extracted_data, "target_job": target_job}
                    response = requests.post(FLASK_ROADMAP_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state.roadmap_data = response.json()
                    else:
                        st.error(f"API Error: {response.json().get('error', 'Unknown error')}")

    # --- Display Suggestions ---
    if st.session_state.suggestions_data:
        st.subheader("🚀 Improvement Suggestions")
        feedback = st.session_state.suggestions_data
        score = feedback.get('resume_score', 0)
        st.metric(label="Resume Score for this Role", value=f"{score}/100")
        st.progress(score)
        st.markdown(f"**Main Feedback:** *{feedback.get('main_feedback')}*")
        for strength in feedback.get('strengths', []):
            st.markdown(f"✅ {strength}")
        # ... (rest of your suggestions display logic) ...

    # --- Display Roadmap ---
    if st.session_state.roadmap_data:
        st.subheader("🗺️ Your Personalized Career Roadmap")
        roadmap_data = st.session_state.roadmap_data
        
        status_map = {
            "completed": "✔",
            "in_progress": "⚙️",
            "to_learn": "📚"
        }
        
        for phase in roadmap_data:
            st.markdown(f"""
            <div class="roadmap-phase">
                <h3>Phase {phase.get('phase')}: {phase.get('title')}</h3>
                <p>{phase.get('summary')}</p>
                <div class="roadmap-steps-container">
                    {''.join([
                        f'<span class="step-tag status-{step.get("status", "to_learn").replace("_", "")}">{status_map.get(step.get("status"), "❓")} {step.get("name")}</span>'
                        for step in phase.get('steps', [])
                    ])}
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Closes main-container