import streamlit as st

def render(go_to_next_page):
    st.title("The Inner Mirror: A Journey to Understanding and Growth")

    with st.form("personal_form"):

        name = st.text_input("1. What's your name or nickname?", placeholder="This could be your full name, a shortened name or whatever feels most 'you'. ")
        age = st.number_input("2. How old are you?", min_value=0, max_value=100)
        gender=st.text_input("3. How do you identify yourself? (Gender)")
        profession = st.text_input("4. What are you currently doing in life?", placeholder="For example: A student ? working ? figuring things out ? somewhere in between?")
        university=st.text_input("5. What is your university or company name?")
        emotion = st.text_area("6. Is there anything on your mind right now ?",placeholder= "You can write about something you're thinking about, feeling, or dealing with - big or small, joyful or stressful. ")
        first_person=st.text_input("6. Who is the first person you reach out to in difficult times?", placeholder="This could be a friend, family member, or anyone you trust.Also write your relationship with them.")
        society = st.text_area("7. Do you find that values like working hard and staying strong make it harder to be gentle with yourself?", placeholder=" We want to understand if focusing on achievement or toughness sometime gets in the way of self-care for you ?")
        family_oriented=st.text_area("8. Do you feel that family expectations or traditions sometimes make it difficult to be kind to yourself ?", placeholder="Sometimes, what's expected at home can affect how we treat ourselves. Let us know if this is true for you.")
        institute_related=st.text_area("9. Are there any rules or ways of doing things in your college/institute that make it tricky to practice being kind to yourself?", placeholder="Sometimes, the way things are done can make self-kindness harder. Please share any experiences like this.")
        submitted = st.form_submit_button("Continue ➡️")

    if submitted and all([name, age, profession,gender, university, emotion, society, family_oriented, institute_related]):
        st.session_state.personal_data = {
            "name": name,
            "age": age,
            "gender":gender,
            "profession": profession,
            "emotion": emotion,
            "first_person": first_person,
            "society": society,
            "family_oriented": family_oriented,
            "institute_related": institute_related,
            "university": university
        }
        go_to_next_page()
        st.rerun()
        
    elif submitted:
        st.warning("Please complete all fields before proceeding.")
