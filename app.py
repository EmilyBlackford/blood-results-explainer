import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import HexColor
import io
import datetime

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

def generate_pdf(results_text, explanation_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#1a73e8'),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#666666'),
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor('#333333'),
        spaceBefore=16,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=HexColor('#222222')
    )
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#888888'),
        leading=13,
        spaceBefore=20
    )

    date_str = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    story = []

    story.append(Paragraph("Blood Results Explainer", title_style))
    story.append(Paragraph(f"Report generated: {date_str}", subtitle_style))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Your Blood Test Results", heading_style))
    for line in results_text.strip().split("\n"):
        if line.strip():
            story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Explanation", heading_style))
    for line in explanation_text.strip().split("\n"):
        if line.strip():
            story.append(Paragraph(line, body_style))
        else:
            story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        "This report is for informational purposes only and does not constitute medical advice. "
        "Always consult a qualified healthcare professional regarding your blood test results.",
        disclaimer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Blood Results Explainer", page_icon="🩺")

st.title("🩺 Blood Results Explainer")
st.markdown("Paste your blood test results below and get a clear, plain-English explanation.")

results_input = st.text_area(
    "Your blood test results",
    height=200,
    placeholder="e.g.\nHaemoglobin: 98 g/L\nWhite Cell Count: 11.8 x10^9/L\nPlatelets: 450 x10^9/L"
)

if st.button("Explain my results"):
    if results_input.strip() == "":
        st.warning("Please paste your blood test results first.")
    else:
        with st.spinner("Analysing your results..."):
            explanation = explain_blood_results(results_input)
        
        st.success("Here's your explanation:")
        st.markdown(explanation)

        st.session_state["explanation"] = explanation
        st.session_state["results"] = results_input

if "explanation" in st.session_state:
    pdf_buffer = generate_pdf(
        st.session_state["results"],
        st.session_state["explanation"]
    )
    st.download_button(
        label="📄 Download as PDF",
        data=pdf_buffer,
        file_name="blood_results_explanation.pdf",
        mime="application/pdf"
    )

st.markdown("---")
st.caption("This tool is for informational purposes only and does not constitute medical advice.")