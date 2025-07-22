# components/start.py
import streamlit as st

def render(go_to_next_page):
    st.title("Start Experiment")
    st.markdown("### Press the button to start the Experiment")

    # Create three columns to center the button. The outer columns act as spacers.
    _ , mid, _ = st.columns([2, 1, 2])
    
    with mid:
        # The button is placed in the middle column
        if st.button("Let's Go", use_container_width=True):
            go_to_next_page()
            st.rerun()