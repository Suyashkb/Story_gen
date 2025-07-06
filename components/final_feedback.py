import streamlit as st
import io, json
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import gspread
from google.oauth2.service_account import Credentials

# --- Helpers ---

def get_gsheet():
    creds = Credentials.from_service_account_info(
        st.secrets["google_sheets"], scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(st.secrets["sheet_id"]).sheet1

def sanitize_pdf_text(text: str) -> str:
    return (text.replace("’", "'").replace("“", '"').replace("”", '"')
                .replace("–", "-").replace("…", "..."))

def sanitize_data(data):
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
    fb = {
        "comfortable": st.text_area("1. How comfortable were you?"),
        "difficulties": st.text_area("2. Any difficulty?"),
        "liked_most": st.text_area("3. What did you like most?"),
        "suggestions": st.text_area("4. Suggestions?")
    }
    if st.button("Finish & Save"):
        st.session_state.final_feedback = fb

        # gather all
        pdata = st.session_state.get("personal_data", {})
        reflections = st.session_state.get("reflections", {})
        quiz_answers = st.session_state.get("quiz_answers", {})
        quiz_scores = st.session_state.get("sc_scores", {})
        story_sections = st.session_state.get("story_sections", [])
        final_fb = fb

        # --- Save to GSheet ---
        sheet = get_gsheet()
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            json.dumps(pdata),
            json.dumps(reflections),
            json.dumps({"answers": quiz_answers, "scores": quiz_scores}),
            json.dumps(story_sections),
            json.dumps(final_fb),
        ]
        try:
            sheet.append_row(row)
            st.success("Saved to Google Sheets 📊")
        except Exception as e:
            st.error(f"Error saving: {e}")

        # --- PDF Generation ---
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
                elif isinstance(content, list):
                    for i, item in enumerate(content, start=1):
                        self.multi_cell(0, 8, f"Scene {i}: {item}")
                else:
                    self.multi_cell(0, 8, str(content))
                self.ln(5)

        pdf = PDF()
        pdf.add_section("Personal Data", sanitize_data(pdata))
        pdf.add_section("Reflections", sanitize_data(reflections))
        pdf.add_section("Quiz Responses & Scores", sanitize_data({"answers": quiz_answers, "scores": quiz_scores}))
        if story_sections:
            pdf.add_section("Generated Story", sanitize_data(story_sections))
        pdf.add_section("Final Feedback", sanitize_data(final_fb))

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("Download PDF report", data=io.BytesIO(pdf_bytes),
                            file_name=f"{pdata.get('name','participant')}_report.pdf", mime="application/pdf")

        # --- CSV Download ---
        csv_rows = []
        def append_csv(section, data):
            if isinstance(data, dict):
                for k,v in data.items():
                    csv_rows.append({"Section": section, "Question": k, "Response": v})
            elif isinstance(data, list):
                for i, v in enumerate(data, start=1):
                    csv_rows.append({"Section": section, "Question": f"Scene {i}", "Response": v})
            else:
                csv_rows.append({"Section": section, "Question": "", "Response": data})

        append_csv("Personal Data", pdata)
        append_csv("Reflections", reflections)
        append_csv("Quiz & Scores", {"answers": quiz_answers, "scores": quiz_scores})
        append_csv("Generated Story", story_sections)
        append_csv("Final Feedback", final_fb)

        df = pd.DataFrame(csv_rows)
        st.download_button("Download CSV", data=df.to_csv(index=False), file_name="results.csv", mime="text/csv")

        st.success("✅ Completed!")
        callback()
        st.stop()
        
        go_to_next_page = st.session_state.get("go_to_next_page", lambda: None)
        st.success("✅ Completed!")
        st.stop()
