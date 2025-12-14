# Resume Analyzer, Improver & Roadmap Generator

![Project Banner](static/project_banner.png)

A powerful AI-powered application that analyzes resumes, provides detailed improvement feedback, and generates personalized career roadmaps. It uses Google's Gemini Pro model for deep analysis and features a modern, interactive Streamlit user interface backed by a robust Flask API.

## Features

- **📄 PDF Resume Analysis**: Instantly extract and analyze key information from PDF resumes.
- **🚀 AI-Powered Feedback**: Get detailed, actionable suggestions to improve your resume score for specific job roles.
- **🗺️ Career Roadmap**: Generate a personalized step-by-step career roadmap to reach your target job.
- **✨ Interactive UI**: A beautiful, responsive Streamlit interface with real-time updates.
- **🔌 Robust API**: A Flask backend handling PDF extraction and AI processing.

## Architecture

The project consists of two main components:
1.  **Backend (Flask)**: Handles file uploads, PDF text extraction, and communication with the Google Gemini API.
2.  **Frontend (Streamlit)**: Provides a user-friendly interface for uploading resumes, viewing results, and interacting with the AI features.

## Prerequisites

- Python 3.x
- Google Generative AI API key

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Aniketp705/resume-analyzer.git
    cd resume-analyzer
    ```

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up environment variables:
    - Create a `.env` file in the project root
    - Add your Google API key:
      ```
      GOOGLE_API_KEY=your_api_key_here
      ```

## Usage

To run the application, you need to start both the Flask backend and the Streamlit frontend.

1.  **Start the Backend Server**:
    Open a terminal and run:
    ```bash
    python app.py
    ```
    The server will start at `http://localhost:5001`.

2.  **Start the Frontend Application**:
    Open a new terminal window (keep the backend running) and run:
    ```bash
    streamlit run sapp.py
    ```
    The application will open in your default web browser (usually at `http://localhost:8501`).

## Project Structure

```
resume-analyzer/
├── app.py                 # Flask Backend API
├── sapp.py                # Streamlit Frontend Application
├── core_logic/
│   ├── analyzer.py        # Resume analysis logic
│   ├── extractor.py       # PDF text extraction
│   └── improver.py        # Feedback and roadmap generation logic
├── static/                # Static assets
├── templates/             # Flask templates (optional)
├── uploaded_resumes/      # Temporary storage for uploads
├── requirements.txt       # Project dependencies
└── readme.md              # Project documentation
```

## API Endpoints

The Flask backend exposes the following endpoints:

-   `POST /analyze`: Upload and analyze a resume PDF.
    -   **Body**: `multipart/form-data` with `resume` file.
-   `POST /suggest-improvements`: Get improvement suggestions for a specific job role.
    -   **Body**: JSON `{ "extracted_data": {...}, "target_job": "..." }`
-   `POST /generate-roadmap`: Generate a career roadmap.
    -   **Body**: JSON `{ "extracted_data": {...}, "target_job": "..." }`

## Contributing

1.  Fork the repository
2.  Create your feature branch
3.  Commit your changes
4.  Push to the branch
5.  Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
