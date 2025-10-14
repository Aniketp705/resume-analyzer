import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import your proven functions
from core_logic.extractor import extract_text_from_pdf
from core_logic.analyzer import analyze_resume_text

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

# --- Route to serve the HTML page ---
@app.route('/')
def index():
    """Renders the main upload page."""
    return render_template('index.html')

# --- API Endpoint ---
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file part in the request"}), 400
    
    file = request.files['resume']

    if not file.filename:
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        extracted_text = extract_text_from_pdf(filepath)
        if not extracted_text:
            return jsonify({"error": "Could not extract text from PDF"}), 500

        analysis_result = analyze_resume_text(extracted_text)
        if analysis_result:
            return jsonify(analysis_result), 200
        else:
            return jsonify({"error": "Failed to analyze the resume with the AI model"}), 500
    else:
        return jsonify({"error": "Invalid file type, only PDFs are allowed"}), 400

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=5001)