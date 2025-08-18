import streamlit as st

def render(go_to_next_page):
    """Renders the start page with detailed instructions for the participant."""
    
    st.title("Welcome to the Experiment 🧠")
    st.markdown("Please read the instructions below carefully before you begin.")
    st.markdown("---")

    # Use an expander for detailed instructions to keep the main page clean.
    with st.expander("Click to Read Experiment Instructions", expanded=True):
        
        st.markdown("### 📜 Experiment Flow")
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

    st.markdown("### Press the button when you're ready to start.")

    # Create columns to center the button
    _ , mid, _ = st.columns([2, 1, 2])
    
    with mid:
        # The button is placed in the middle column
        if st.button("Let's Go!", use_container_width=True, type="primary"):
            go_to_next_page()
            st.rerun()