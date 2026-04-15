import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain_blood_results(results_text):
    prompt = """
You are a helpful medical assistant explaining blood test results to a patient.

The patient has shared the following blood test results:
""" + results_text + """

Please:
1. Explain what each value means in plain English
2. Flag any results that appear abnormal (high or low)
3. Use simple, reassuring language a non-medical person would understand
4. Add a clear safety disclaimer at the end

Do not diagnose any conditions. Always recommend consulting a doctor.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def main():
    print("🩺 Blood Results Explainer")
    print("=" * 40)
    print("Paste your blood test results below.")
    print("Type 'DONE' on a new line when finished.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    results = "\n".join(lines)

    print("\n⏳ Analysing your results...\n")
    explanation = explain_blood_results(results)
    print(explanation)

if __name__ == "__main__":
    main()