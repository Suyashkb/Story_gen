import streamlit as st

def render(go_to_next_page):
    st.set_page_config(page_title="Self-Compassion Quiz", layout="centered")
    st.title("🧠 Self-Compassion Quiz")

    st.markdown("""
    #### 📝 Before you begin:
    This questionnaire has **no right or wrong answers**.  
    Please reflect honestly. Your responses will shape the emotional tone of your personalized story.
    """)

    # Add CSS to reduce spacing between question and options
    st.markdown("""
    <style>
    .stRadio > div {
        gap: 0.25rem !important;
        margin-bottom: 1.25rem;
    }
    .question-label {
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 4px;
        color: inherit !important;
    }
    </style>
    """, unsafe_allow_html=True)


    positive_scoring = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    negative_scoring = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

    scoring_groups = {
        "Self-Kindness":     ["SK1", "SK2"],
        "Self-Judgment":     ["SJ1", "SJ2"],
        "Common Humanity":   ["CH1", "CH2"],
        "Isolation":         ["IS1", "IS2"],
        "Mindfulness":       ["MF1", "MF2"],
        "Overidentification": ["OID1", "OID2"]
    }

    questions = {
        "SK1": "I try to be understanding and patient towards those aspects of my personality I don’t like.", 
        "SK2": "When I’m going through a very hard time, I give myself the caring and tenderness I need.",
        "SJ1": "I’m disapproving and judgmental about my own flaws and inadequacies.",
        "SJ2": "I’m intolerant and impatient towards those aspects of my personality I don’t like.",
        "CH1": "I try to see my failings as part of the human condition.",
        "CH2": "When I feel inadequate in some way, I try to remind myself that feelings of inadequacy are shared by most people.",
        "IS1": "When I’m feeling down, I tend to feel like most other people are probably happier than I am.",
        "IS2": "When I fail at something that’s important to me, I tend to feel alone in my failure.",
        "MF1": "When something painful happens I try to take a balanced view of the situation.",
        "MF2": "When something upsets me I try to keep my emotions in balance.",
        "OID1": "When I fail at something important to me I become consumed by feelings of inadequacy.",
        "OID2": "When I’m feeling down I tend to obsess and fixate on everything that’s wrong.",
    }

    option_labels = [
        "A. Strongly Agree",
        "B. Agree",
        "C. Neither Agree nor Disagree",
        "D. Disagree",
        "E. Strongly Disagree"
    ]

    with st.form("quiz_form"):
        answers = {}
        for q_key, q_text in questions.items():
            st.markdown(f"<div class='question-label'>{q_text}</div>", unsafe_allow_html=True)
            selected = st.radio(
                label="",  # Don't repeat the question
                options=option_labels,
                key=q_key,
                index=None,
                label_visibility="collapsed"
            )
            if selected:
                answers[q_key] = selected[0]


        quiz_submitted = st.form_submit_button("Finish Quiz ✅")

    def calculate_self_compassion_scores(answers):
        def get_score(keys, scoring):
            return sum(scoring[answers[k]] for k in keys)

        return {
            "Self-Kindness vs Self-Judgment":
                get_score(scoring_groups["Self-Kindness"], positive_scoring) +
                get_score(scoring_groups["Self-Judgment"], negative_scoring),
            "Common Humanity vs Isolation":
                get_score(scoring_groups["Common Humanity"], positive_scoring) +
                get_score(scoring_groups["Isolation"], negative_scoring),
            "Mindfulness vs Overidentification":
                get_score(scoring_groups["Mindfulness"], positive_scoring) +
                get_score(scoring_groups["Overidentification"], negative_scoring),
        }

    if quiz_submitted:
        if len(answers) == len(questions):
            st.session_state.quiz_answers = answers
            st.session_state.sc_scores = calculate_self_compassion_scores(answers)

            st.success("✅ Quiz submitted successfully!")
            st.button("Continue to Story ➡️", on_click=go_to_next_page)
            st.success("Please wait for 1–2 minutes while your story is being generated...")
        else:
            st.warning("Please answer all the questions to continue.")
