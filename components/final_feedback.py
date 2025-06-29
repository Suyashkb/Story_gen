import streamlit as st
import io
from gtts import gTTS
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fpdf import FPDF
import json
import pandas as pd

load_dotenv()

# Access the API key
api_key = os.getenv("GOOGLE_API_KEY")

# Check if the key is available
if not api_key:
    st.error("GOOGLE_API_KEY environment variable not set.")
    st.stop()

# Configure the GenAI client
genai.configure(api_key=api_key)

def render(go_to_next_page):
    st.markdown("## 🧠 Final Feedback")
    st.write("Please share your experience with the experiment.")

    # Feedback Questions
    q1 = st.text_area("1. How comfortable were you during the experiment?", key="fb_q1")
    q2 = st.text_area("2. Did you face any difficulty in understanding or responding?", key="fb_q2")
    q3 = st.text_area("3. What did you like the most about the experience?", key="fb_q3")
    q4 = st.text_area("4. Any suggestions for improvement?", key="fb_q4")

    st.session_state["final_feedback"] = {
        "comfort_level": q1,
        "difficulties_faced": q2,
        "liked_most": q3,
        "suggestions": q4
    }
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)
            self.set_font("Times", size=15)

        def chapter_title(self, title):
            self.set_font("Times", "B", 13)
            self.cell(0, 10, title, ln=True, align='L')

        def chapter_body(self, body):
            self.set_font("Times", "", 11)
            self.multi_cell(0, 10, body)

        def add_section(self, title, content_dict):
            self.chapter_title(title)
            for k, v in content_dict.items():
                self.chapter_body(f"{k}: {v}")
                
    st.success("Thank you for your feedback! Your responses will be used to improve the experiment.")
    st.success("Your experiment is now complete! ")

    st.markdown("## Download Your Responses")

    # Gather all data
    pdata = st.session_state.get("personal_data", {})
    reflections = st.session_state.get("reflections", {})
    quiz_answers = st.session_state.get("quiz_answers", {})
    quiz_scores = st.session_state.get("sc_scores", {})
    story_sections = st.session_state.get("story_sections", [])
    final_feedback = st.session_state.get("final_feedback", {})

    # 1. JSON Export
    export_data = {
        "personal_data": pdata,
        "stories": story_sections,
        "reflections": reflections,
        "self_compassion_quiz": {
            "answers": quiz_answers,
            "scores": quiz_scores
        },
        "final_feedback": final_feedback
    }

    st.download_button(
        "📁 Download as JSON",
        data=json.dumps(export_data, indent=2),
        file_name="reflection_summary.json"
    )
            
    # Function to generate PDF content
    #2. PDF Export
    def generate_pdf():
        pdf = PDF()
        pdf.add_page()

        # Personal Data
        pdf.add_section("Personal Data", pdata)

        # Reflections
        pdf.add_section("Reflections", reflections)

        # Quiz Answers
        if quiz_answers:
            pdf.add_section("Self-Compassion Quiz Answers", quiz_answers)

        # Quiz Scores
        if quiz_scores:
            pdf.add_section("Self-Compassion Quiz Scores", quiz_scores)

        # Add LLM-generated story scenes
        if story_sections:
            pdf.chapter_title("Generated Story")
            for i, scene in enumerate(story_sections):
                pdf.chapter_body(f"Scene {i+1}: {scene}")

        # Final Feedback
        if final_feedback:
            pdf.add_section("Final Feedback", final_feedback)

        # Generate and return the PDF in memory
        pdf_output = pdf.output(dest='S').encode('latin-1')
        return io.BytesIO(pdf_output)

    # Get participant name for file naming
    participant_name = pdata.get("name", "participant").strip().replace(" ", "_")
    pdf_file_name = f"Summary_{participant_name}.pdf"

    # ✅ PDF Download Button (single button!)
    st.download_button(
        label="📄 Download as PDF",
        data=generate_pdf(),
        file_name=pdf_file_name,
        mime="application/pdf"
    )

    # Function to generate CSV content
    def generate_csv():
        csv_data = []

        def append_section(section_name, data_dict):
            for k, v in data_dict.items():
                csv_data.append({
                    "Section": section_name,
                    "Question": k,
                    "Response": v
                })

        append_section("Personal Data", pdata)
        append_section("Reflections", reflections)
        append_section("Self-Compassion Quiz Answers", quiz_answers)
        append_section("Self-Compassion Quiz Scores", quiz_scores)
        append_section("Final Feedback", final_feedback)

        if story_sections:
            for i, section in enumerate(story_sections):
                csv_data.append({
                    "Section": "Generated Story",
                    "Question": f"Scene {i+1}",
                    "Response": section
                })

        df = pd.DataFrame(csv_data)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()

    # ✅ CSV Download Button (single button!)
    st.download_button(
        label="📊 Download as CSV (Google Sheets Compatible)",
        data=generate_csv(),
        file_name="reflection_summary.csv",
        mime="text/csv"
    )
    
   