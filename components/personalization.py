import streamlit as st

def render(go_to_next_page):
    st.title("Let's Personalize Your Experience")

    with st.form("personal_form"):
        st.subheader("Individual Profile")
        name = st.text_input("1. What's your name or nickname?")
        age = st.number_input("2. How old are you?", min_value=10, max_value=100)
        profession = st.text_input("3. What do you do (student/professional/other)?")
        emotion = st.text_input("4. What's your current emotion or mood?")
        st.markdown("_Tip: You can use a color to describe your emotion. For example: red=anger, blue=sadness, yellow=joy._")
        issue = st.text_area("5. Is there anything on your mind or something you're dealing with?")

        st.markdown("---")
        st.subheader("Socio-Cultural Context")
        influencer = st.text_input("6. Who has been the most influential figure in your life?")
        social_pressure = st.text_input("7. Are there societal pressures you experience?")
        expectation = st.text_input("8. Do you feel burdened by expectations (family/society)?")

        submitted = st.form_submit_button("Continue ➡️")

    if submitted and all([name, age, profession, emotion, issue, influencer, social_pressure, expectation]):
        st.session_state.personal_data = {
            "name": name,
            "age": age,
            "profession": profession,
            "emotion": emotion,
            "issue": issue,
            "influencer": influencer,
            "social_pressure": social_pressure,
            "expectation": expectation
        }
        go_to_next_page()
        st.rerun()
        
    elif submitted:
        st.warning("Please complete all fields before proceeding.")
