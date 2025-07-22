# main.py
import streamlit as st
from components import personalization, mindfulness, quiz, story, final_feedback, start  # Add 'start'

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "personalization"

# Define navigation logic
def go_to_next_page():
    if st.session_state.page == "personalization":
        st.session_state.page = "quiz"
    elif st.session_state.page == "quiz":
        st.session_state.page = "start"
    elif st.session_state.page == "start":
        st.session_state.page = "mindfulness"
    elif st.session_state.page == "mindfulness":
        st.session_state.page = "story"
    elif st.session_state.page == "story":
        st.session_state.page = "final_feedback"

# Render pages
if st.session_state.page == "personalization":
    personalization.render(go_to_next_page)

elif st.session_state.page == "quiz":
    quiz.render(go_to_next_page)

elif st.session_state.page == "start":
    start.render(go_to_next_page)

elif st.session_state.page == "mindfulness":
    mindfulness.render(go_to_next_page)

elif st.session_state.page == "story":
    story.render(go_to_next_page)

elif st.session_state.page == "final_feedback":
    final_feedback.render(go_to_next_page)

else:
    st.error("You are done !!")