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
    
    /* Base button styling */
    div[data-testid="stButton"] > button {
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(-1px);
    }

    /* Primary button (Analyze) */
    div[data-testid="stFileUploader"] + div[data-testid="stButton"] > button {
        background: linear-gradient(45deg, #6366f1, #8b5cf6);
    }
    div[data-testid="stFileUploader"] + div[data-testid="stButton"] > button:hover {
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
    }

    /* Suggestion button */
    [data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stButton"] > button {
        background: linear-gradient(45deg, #10B981, #34D399);
    }
    [data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stButton"] > button:hover {
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4);
    }

    /* Roadmap button */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button {
        background: linear-gradient(45deg, #F59E0B, #FBBF24);
    }
    [data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button:hover {
        box-shadow: 0 10px 20px rgba(245, 158, 11, 0.4);
    }

    /* --- File Uploader --- */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #4a5568;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1.5rem; border-radius: 12px;
    }
    
    /* --- Roadmap Styles --- */
    .roadmap-phase {
        background-color: rgba(26, 32, 44, 0.7);
        border: 1px solid #2d3748; border-radius: 12px;
        padding: 1.5rem; margin-bottom: 1.5rem; animation: fadeIn 1s ease-out;
    }
    .roadmap-phase h3 { font-size: 1.5rem; font-weight: 600; color: #ffffff; margin-top: 0; }
    .roadmap-phase p { font-size: 1rem; color: #a0aec0; margin-bottom: 1.5rem; }
    .roadmap-steps-container { display: flex; flex-wrap: wrap; gap: 0.75rem; }
    .step-tag {
        display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.4rem 1rem;
        border-radius: 16px; font-size: 0.9rem; font-weight: 500; border: 1px solid;
    }
    .status-completed { background-color: rgba(56, 161, 105, 0.1); color: #68d391; border-color: #38a169; }
    .status-in_progress { background-color: rgba(221, 107, 32, 0.1); color: #f6ad55; border-color: #dd6b20; }
    .status-to_learn { background-color: #2d3748; color: #a0aec0; border-color: #4a5568; }

    /* --- Styling for Disabled Form Fields (Profile Display) --- */
    div[data-testid="stTextInput"] input[disabled],
    div[data-testid="stTextArea"] textarea[disabled] {
        color: #e2e8f0 !important; 
        -webkit-text-fill-color: #e2e8f0 !important;
        background-color: #2d3748;
        border: 1px solid #4a5568;
        opacity: 1; /* Override Streamlit's default disabled opacity */
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label {
        color: #a0aec0;
        font-weight: 500;
    }
    
    /* --- Skill Tags in Suggestion Box --- */
    .skill-tag {
        background-color: #2d3748; color: #e2e8f0; padding: 0.4rem 1rem; border-radius: 16px;
        font-size: 0.9rem; font-weight: 500; transition: transform 0.2s ease, background-color 0.2s ease;
        display: inline-block; /* Make span behave like a block */
        margin: 0.25rem; /* Add spacing */
    }
    .skill-tag:hover { transform: scale(1.08); background-color: #4a5568; }
"""
st.markdown(f'<style>{page_style}</style>', unsafe_allow_html=True)

# --- API Endpoints ---
FLASK_ANALYZE_URL = "http://127.0.0.1:5001/analyze"
FLASK_SUGGEST_URL = "http://127.0.0.1:5001/suggest-improvements"
FLASK_ROADMAP_URL = "http://127.0.0.1:5001/generate-roadmap"

# --- Session State Initialization ---
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'suggestions_data' not in st.session_state:
    st.session_state.suggestions_data = None
if 'roadmap_data' not in st.session_state:
    st.session_state.roadmap_data = None

# --- Main App Container ---
# st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("📄 AI Resume Analyzer, Improver & Roadmap Generator")
st.markdown("Upload a resume, get suggestions, and generate a career roadmap.")

# --- Step 1: File Upload (Fast Extraction) ---
uploaded_file = st.file_uploader(
    "Step 1: Upload your resume PDF for analysis.",
    type="pdf",
    label_visibility="collapsed"
)

# This logic automatically triggers analysis on new file upload
if uploaded_file is not None:
    # Check if this is a new file or the same one
    if st.session_state.extracted_data is None or st.session_state.extracted_data.get('filename') != uploaded_file.name:
        with st.spinner("Analyzing (Fast)... Please wait."):
            try:
                files = {'resume': (uploaded_file.name, uploaded_file, 'application/pdf')}
                response = requests.post(FLASK_ANALYZE_URL, files=files)
                
                if response.status_code == 200:
                    st.success("Analysis Complete!")
                    st.session_state.extracted_data = response.json()
                    st.session_state.extracted_data['filename'] = uploaded_file.name # Tag with filename
                    st.session_state.suggestions_data = None 
                    st.session_state.roadmap_data = None 
                else:
                    st.session_state.extracted_data = None
                    st.error(f"API Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException:
                st.session_state.extracted_data = None
                st.error("Connection Error: Could not connect to the backend.")

# --- Display Extracted Data as a Form ---
if st.session_state.extracted_data:
    result = st.session_state.extracted_data
    
    st.subheader("📄 Extracted Resume Profile")
    personal = result.get('personal_details', {})
    skills = result.get('skills', [])
    summary = result.get('professional_summary', "Not found.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Name", personal.get('name'), disabled=True)
        st.text_input("Email", personal.get('email'), disabled=True)
    with col2:
        st.text_input("Phone", personal.get('phone_number'), disabled=True)
        st.text_input("Location", personal.get('location'), disabled=True)

    st.text_area("Skills", ", ".join(skills) if skills else "Not found.", height=125, disabled=True)
    st.text_area("Professional Summary", summary, height=150, disabled=True)
    
    with st.expander("Show Full Work History & Education (Raw Data)"):
        st.json({
            "work_experience": result.get('work_experience', []),
            "education": result.get('education', [])
        })

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
        if st.button("Get Improvement Suggestions (Pro)", key="btn_get_suggestions", use_container_width=True):
            if not target_job.strip():
                st.error("Please enter a target job profile.")
            else:
                with st.spinner("Our AI Coach is thinking... Please wait."):
                    payload = {"extracted_data": st.session_state.extracted_data, "target_job": target_job}
                    response = requests.post(FLASK_SUGGEST_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state.suggestions_data = response.json()
                        st.session_state.roadmap_data = None # Clear other result
                    else:
                        st.error(f"API Error: {response.json().get('error', 'Unknown error')}")

    with col2:
        if st.button("Generate Career Roadmap (Pro)", key="btn_get_roadmap", use_container_width=True):
            if not target_job.strip():
                st.error("Please enter a target job profile.")
            else:
                with st.spinner("Generating your personalized roadmap..."):
                    payload = {"extracted_data": st.session_state.extracted_data, "target_job": target_job}
                    response = requests.post(FLASK_ROADMAP_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state.roadmap_data = response.json()
                        st.session_state.suggestions_data = None # Clear other result
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
        
        st.markdown("<h5>Strengths:</h5>", unsafe_allow_html=True)
        for strength in feedback.get('strengths', []):
            st.markdown(f"✅ {strength}")
        
        st.markdown("<h5>Top 3 Improvements:</h5>", unsafe_allow_html=True)
        for improvement in feedback.get('top_3_improvements', []):
            with st.expander(f"**{improvement.get('area')}**"):
                st.markdown(f"**Suggestion:** {improvement.get('suggestion')}")
                if 'example_rewrite' in improvement:
                    st.code(improvement['example_rewrite'], language='text')
                if 'examples' in improvement:
                    st.markdown("**Weak Verbs:** " + ", ".join(improvement['examples']['weak_verbs']))
                    st.markdown("**Stronger Verbs:** " + ", ".join(improvement['examples']['stronger_verbs']))
                if 'keywords_to_add' in improvement:
                    st.markdown("**Keywords to Add:**")
                    st.markdown(" ".join([f'<span class="skill-tag status-to_learn">{kw}</span>' for kw in improvement['keywords_to_add']]), unsafe_allow_html=True)

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