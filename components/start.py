import streamlit as st

def render(go_to_next_page):
    """Renders the start page with a consent form and detailed instructions."""
    
    st.title("Welcome to the Experiment ")
    st.markdown("Please read the following information carefully before you begin.")
    st.markdown("---")

    # --- Consent Form Section ---
    st.subheader("Consent to Participate in Research")
    
    st.info(
        """
        **Purpose of the Research:** This study aims to investigate brain activity during emotional and cognitive tasks.
        
        **Procedures:** You will be fitted with an EEG and fNIRS cap to measure your brain's electrical and blood flow activity. You will then be asked to perform a series of tasks, including reading stories and answering questions about your experience. The entire session will last approximately 35 minutes.
        
        **Nature:** This in non-diagnostic and non-therapeutic research. No medical or psychological treatment will be provided.
        
        **Risks:** It is a non-invasive procedure with minimal risk. You may experience slight discomfort from wearing the cap, but there are no known risks associated with EEG or fNIRS.

        **Confidentiality and Anonymity:** Your participation will be kept strictly confidential. All data collected, including your brain activity recordings and your responses, will be **anonymized**. Your name or any personal identifiers will not be linked to the data in any publication or presentation. The anonymous data will be used solely for academic research purposes.

        **Voluntary Participation:** Your participation in this study is completely voluntary. You are free to withdraw at any time without any penalty.
        
        

        By checking the box below, you acknowledge that you have read and understood the information above and voluntarily agree to participate.
        """
    )

    # --- Checkbox for Consent ---
    # The user must check this box to proceed.
    consent_given = st.checkbox("**I have read and understood the information above and I consent to participate in this study.**")
    
    st.markdown("---")


    # Use an expander for detailed instructions to keep the main page clean.
    with st.expander("Click to Read Experiment Instructions", expanded=True):
        
        st.markdown("### 📋 Experiment Flow")
        st.markdown("""
        1.  **Baseline Phase:** We'll begin by recording your baseline brain activity with simple tasks like opening and closing your eyes.
        2.  **Story Scenes:** You will read several stories presented in short paragraphs. Click the **'Next Section'** button to advance through each story.
        3.  **Emotional Response:** After each story, you will be asked questions about your feelings. Please answer them in **at least 2-3 lines**.
        4.  **Final Review:** At the very end, you'll complete a short review about your experience.
        5.  **Save Your Data:** This is a crucial final step! Please press the **'Save Data'** button on the last page to ensure your participation is recorded.
        """)

        st.markdown("### ⚠️ Important: For High-Quality Data")
        st.warning("""
        You are wearing an **EEG and fNIRS cap** to measure brain activity. To get clear data, it is essential to **minimize all movement**. Please try your best to:
        
        - Remain seated and keep your head and body as still as possible.
        - Relax your facial muscles and **avoid clenching your jaw**.
        - Keep your legs and feet still.
        - **Try to blink less often**, especially while reading the stories.
        """)

    st.markdown("### Please provide consent and press the button when you're ready.")
    
    # --- Conditional Button Logic ---
    # The button will be disabled until the consent checkbox is ticked.
    if not consent_given:
        st.warning("You must provide your consent before you can begin the experiment.")

    _ , mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("Let's Go!", use_container_width=True, type="primary", disabled=not consent_given):
            go_to_next_page()
            st.rerun()