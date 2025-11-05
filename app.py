import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import your proven functions
from core_logic.extractor import extract_text_from_pdf
# 1. Import BOTH analyzer functions
from core_logic.analyzer import extract_resume_data
from core_logic.improver import get_resume_feedback, get_career_roadmap

# --- Configuration ---
UPLOAD_FOLDER = 'uploaded_resumes'
ALLOWED_EXTENSIONS = {'pdf'}

# --- Flask App Setup ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# --- Helper Function ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Route to serve the HTML page (Optional for Postman testing) ---
@app.route('/')
def index():
    """Renders the main upload page."""
    return render_template('index.html')

# --- API Endpoint 1: FAST EXTRACTION (Flash) ---
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    # This endpoint only needs the resume file
    if 'resume' not in request.files:
        return jsonify({"error": "No 'resume' file part in the request"}), 400

    file = request.files['resume']

    if not file.filename:
        return jsonify({"error": "No resume file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(filepath)
        except Exception as e:
             return jsonify({"error": f"Failed to save file: {e}"}), 500

        extracted_text = extract_text_from_pdf(filepath)
        if not extracted_text:
            return jsonify({"error": "Could not extract text from PDF"}), 500

        # Call the FAST analyzer function
        analysis_result = extract_resume_data(extracted_text)
        
        if analysis_result:
            return jsonify(analysis_result), 200
        else:
            return jsonify({"error": "Failed to analyze the resume with the AI model"}), 500
    else:
        return jsonify({"error": "Invalid file type, only PDFs are allowed"}), 400

# --- API Endpoint 2: DEEP FEEDBACK (Pro) ---
@app.route('/suggest-improvements', methods=['POST'])
def suggest_improvements():
    # This endpoint expects JSON data, not form data
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    extracted_data = data.get('extracted_data')
    target_job = data.get('target_job')

    if not extracted_data or not target_job:
        return jsonify({"error": "Missing 'extracted_data' or 'target_job' in JSON body"}), 400

    # Call the POWERFUL improver function
    feedback_result = get_resume_feedback(extracted_data, target_job)

    if feedback_result:
        return jsonify(feedback_result), 200
    else:
        return jsonify({"error": "Failed to get improvement suggestions"}), 500
    
@app.route('/generate-roadmap', methods=['POST'])
def generate_roadmap_endpoint():
    data = request.get_json()
    if not data or 'extracted_data' not in data or 'target_job' not in data:
        return jsonify({"error": "Missing 'extracted_data' or 'target_job' in JSON body"}), 400
    
    extracted_data = data.get('extracted_data')
    target_job = data.get('target_job')

    # Call a new function from your "improver" module
    roadmap_json = get_career_roadmap(extracted_data, target_job)
    
    if roadmap_json:
        return jsonify(roadmap_json), 200
    else:
        return jsonify({"error": "Failed to generate career roadmap"}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5001)
