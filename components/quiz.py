import streamlit as st

def render(go_to_next_page):
    st.set_page_config(page_title="Self-Compassion Quiz", layout="centered")
    st.title("🧠 Self-Compassion Quiz")

    st.markdown("""
    #### 📝 Before you begin:
    This questionnaire has **no right or wrong answers**.  
    Please reflect honestly on how you typically act towards yourself in difficult times. Your responses will shape the emotional tone of your personalized story.
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

    # --- UPDATED: New scoring groups for 26 questions ---
    scoring_groups = {
        "Self-Kindness":      ["Q5", "Q12", "Q19", "Q23", "Q26"],
        "Self-Judgment":      ["Q1", "Q8", "Q11", "Q16", "Q21"],
        "Common Humanity":    ["Q3", "Q7", "Q10", "Q15"],
        "Isolation":          ["Q4", "Q13", "Q18", "Q25"],
        "Mindfulness":        ["Q9", "Q14", "Q17", "Q22"],
        "Overidentification": ["Q2", "Q6", "Q20", "Q24"]
    }

    # --- UPDATED: New list of 26 questions ---
    questions = {
        "Q1": "I’m disapproving and judgmental about my own flaws and inadequacies.",
        "Q2": "When I’m feeling down I tend to obsess and fixate on everything that’s wrong.",
        "Q3": "When things are going badly for me, I see the difficulties as part of life that everyone goes through.",
        "Q4": "When I think about my inadequacies, it tends to make me feel more separate and cut off from the rest of the world.",
        "Q5": "I try to be loving towards myself when I’m feeling emotional pain.",
        "Q6": "When I fail at something important to me I become consumed by feelings of inadequacy.",
        "Q7": "When I'm down, I remind myself that there are lots of other people in the world feeling like I am.",
        "Q8": "When times are really difficult, I tend to be tough on myself.",
        "Q9": "When something upsets me I try to keep my emotions in balance.",
        "Q10": "When I feel inadequate in some way, I try to remind myself that feelings of inadequacy are shared by most people.",
        "Q11": "I’m intolerant and impatient towards those aspects of my personality I don't like.",
        "Q12": "When I’m going through a very hard time, I give myself the caring and tenderness I need.",
        "Q13": "When I’m feeling down, I tend to feel like most other people are probably happier than I am.",
        "Q14": "When something painful happens I try to take a balanced view of the situation.",
        "Q15": "I try to see my failings as part of the human condition.",
        "Q16": "When I see aspects of myself that I don’t like, I get down on myself.",
        "Q17": "When I fail at something important to me I try to keep things in perspective.",
        "Q18": "When I’m really struggling, I tend to feel like other people must be having an easier time of it.",
        "Q19": "I’m kind to myself when I’m experiencing suffering.",
        "Q20": "When something upsets me I get carried away with my feelings.",
        "Q21": "I can be a bit cold-hearted towards myself when I'm experiencing suffering.",
        "Q22": "When I'm feeling down I try to approach my feelings with curiosity and openness.",
        "Q23": "I’m tolerant of my own flaws and inadequacies.",
        "Q24": "When something painful happens I tend to blow the incident out of proportion.",
        "Q25": "When I fail at something that's important to me, I tend to feel alone in my failure.",
        "Q26": "I try to be understanding and patient towards those aspects of my personality I don't like."
    }

    option_labels = [
        "A. Almost never",
        "B. Rarely",
        "C. Sometimes",
        "D. Often",
        "E. Almost always"
    ]

    with st.form("quiz_form"):
        answers = {}
        # The loop now iterates through all 26 questions
        for q_key, q_text in questions.items():
            st.markdown(f"<div class='question-label'>{q_text}</div>", unsafe_allow_html=True)
            selected = st.radio(
                label=q_text, # Accessibility label
                options=option_labels,
                key=q_key,
                index=None,
                label_visibility="collapsed"
            )
            if selected:
                answers[q_key] = selected[0]


        quiz_submitted = st.form_submit_button("Finish Quiz ✅")

    # This function works perfectly with the new data, no changes needed
    def calculate_self_compassion_scores(answers):
        def get_score(keys, scoring):
            # Ensures a score of 0 if a question hasn't been answered yet
            return sum(scoring.get(answers.get(k), 0) for k in keys)

        # The calculation remains the same, but it now uses the new scoring_groups
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
            st.button("Continue", on_click=go_to_next_page)

        else:
            st.warning("Please answer all 26 questions to continue.")
