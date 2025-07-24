import streamlit as st
import io, json
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import gspread
from google.oauth2.service_account import Credentials

# --- Helpers (assuming they are defined as before) ---

def get_gsheet():
    creds = Credentials.from_service_account_info(
        st.secrets["google_sheets"], scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(st.secrets["sheet_id"]).sheet1

def sanitize_pdf_text(text: str) -> str:
    original = text
    text = (text.replace("’", "'").replace("‘", "'")
                .replace("“", '"').replace("”", '"')
                .replace("–", "-").replace("…", "..."))
    try:
        return text.encode("latin-1").decode("latin-1")
    except UnicodeEncodeError:
        print("⚠️ Skipped some characters in:", original)
        return text.encode("latin-1", "ignore").decode("latin-1")

def sanitize_data(data):
    # ... (sanitize function remains the same)
    if isinstance(data, str):
        return sanitize_pdf_text(data)
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_data(v) for v in data]
    return data


# --- Main Render Function ---
def render(go_to_next_page):
    st.header("🧠 Final Feedback")
    st.write("Your anonymous feedback is valuable for improving this experience.")
    
    fb = {
        "comfortable": st.text_area("1. How comfortable were you during this narrative experience?"),
        "difficulties": st.text_area("2. Did you face any difficulties or find any part confusing?"),
        "liked_most": st.text_area("3. What did you like most about the story or the process?"),
        "suggestions": st.text_area("4. Do you have any suggestions for improvement?")
    }

    if st.button("Finish & Save Report"):
        st.session_state.final_feedback = fb

        # --- Gather all data from session state ---
        pdata = st.session_state.get("personal_data", {})
        reflections = st.session_state.get("reflections", {})
        quiz_answers = st.session_state.get("quiz_answers", {})
        quiz_scores = st.session_state.get("sc_scores", {})
        
        # ✅ CORRECTED: Use 'story_text' to get the generated stories
        story_text_data = st.session_state.get("story_text", {}) 
        
        final_fb = fb

        with st.spinner("Saving your report..."):
            # --- 1. Save to Google Sheets ---
            try:
                sheet = get_gsheet()
                row_to_append = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    json.dumps(pdata),
                    json.dumps({"answers": quiz_answers, "scores": quiz_scores}),
                    json.dumps(story_text_data),
                    json.dumps(reflections),
                    json.dumps(final_fb),
                ]
                sheet.append_row(row_to_append)
                st.success("Your anonymous responses have been saved. Thank you!")
            except Exception as e:
                st.error(f"Could not save data to the sheet. Error: {e}")

            # --- 2. PDF Generation ---
            class PDF(FPDF):
                def __init__(self):
                    super().__init__()
                    self.set_auto_page_break(True, 15)
                    self.add_page()
                    self.set_font("Times", size=12)
                def add_section(self, title, content):
                    self.set_font("Times", "B", 14)
                    self.cell(0, 10, title, ln=1)
                    self.set_font("Times", "", 12)
                    if isinstance(content, dict):
                        for k,v in content.items():
                            self.multi_cell(0, 8, f"{k}: {v}")
                    else:
                        self.multi_cell(0, 8, str(content))
                    self.ln(5)

            pdf = PDF()
            pdf.add_section("Personal Data", sanitize_data(pdata))
            pdf.add_section("Quiz Responses & Scores", sanitize_data({"answers": quiz_answers, "scores": quiz_scores}))
            pdf.add_section("Reflections", sanitize_data(reflections))
            # ✅ CORRECTED: Add the story section to the PDF
            if story_text_data:
                pdf.add_section("Generated Story Scenes", sanitize_data(story_text_data))
            pdf.add_section("Final Feedback", sanitize_data(final_fb))

            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                "⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"{pdata.get('name', 'participant').replace(' ', '_')}_report.pdf",
                mime="application/pdf"
            )

            st.info("Thank you for participating in the experiment!")
            st.stop()

