# Resume Analyzer

A Flask-based web application that analyzes resumes using Google's Gemini Pro AI model to extract and analyze key information from PDF resumes.

## Features

- PDF resume upload functionality
- Automatic text extraction from PDF files
- AI-powered resume analysis using Google's Gemini Pro
- Clean and simple web interface
- Cross-origin resource sharing (CORS) enabled

## Prerequisites

- Python 3.x
- Flask
- PyMuPDF (fitz)
- Google Generative AI API key
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aniketp705/resume-analyzer.git
cd resume-analyzer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Project Structure

```
resume-analyzer/
├── app.py                 # Main Flask application
├── core_logic/
│   ├── analyzer.py       # Resume analysis logic using Gemini Pro
│   └── extractor.py      # PDF text extraction functionality
├── static/
│   └── style.css         # CSS styles for the web interface
├── templates/
│   └── index.html        # HTML template for the upload page
└── uploaded_resumes/     # Directory for temporary resume storage
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open a web browser and navigate to `http://localhost:5001`

3. Upload a PDF resume and click "Analyze" to get the AI-powered analysis

## API Endpoints

- `GET /`: Serves the main upload page
- `POST /analyze`: Accepts PDF resume uploads and returns analysis results
  - Request: multipart/form-data with 'resume' file field
  - Response: JSON containing analyzed resume data

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- Missing files
- PDF extraction errors
- API configuration issues
- Analysis failures

## Security Features

- Secure filename handling
- File type validation
- Controlled upload directory
- CORS protection

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
