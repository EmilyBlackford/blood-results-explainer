# 🩺 Blood Results Explainer

A Python web application that explains blood test results in plain, patient-friendly English using AI.

## What it does

- Accepts blood test results pasted as plain text
- Uses Google Gemini AI to explain what each value means
- Flags any abnormal results clearly
- Generates a downloadable PDF report
- Includes appropriate medical safety disclaimers

## Technologies used

- **Python** — core programming language
- **Google Gemini API** — large language model for interpreting results
- **Streamlit** — web interface framework
- **ReportLab** — PDF generation
- **python-dotenv** — secure API key management

## How to run locally

### Prerequisites
- Python 3.10+
- A free Google Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### Setup

1. Clone the repository
```bash
   git clone https://github.com/EmilyBlackford/blood-results-explainer.git
   cd blood-results-explainer
```

2. Create and activate a virtual environment
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies
```bash
   pip install streamlit google-genai python-dotenv reportlab
```

4. Create a `.env` file in the project root
GEMINI_API_KEY=your-api-key-here

5. Run the app
```bash
   streamlit run app.py
```

6. Open your browser at `http://localhost:8501`

## Example input
Haemoglobin: 98 g/L
White Cell Count: 11.8 x10^9/L
Platelets: 450 x10^9/L
Ferritin: 6 ug/L
CRP: 28 mg/L

## Disclaimer

This tool is for informational purposes only and does not constitute medical advice. Always consult a qualified healthcare professional regarding your blood test results.

## Author

Emily Blackford — iOS Developer exploring AI engineering