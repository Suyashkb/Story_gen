import streamlit as st
import time

def render(go_to_next_page):
    st.title("Mindfulness Activity")

    if "mindfulness_stage" not in st.session_state:
        st.session_state.mindfulness_stage = "intro"

    # Stage 1: Eyes closed
    if st.session_state.mindfulness_stage == "intro":
        st.markdown("## Get ready for the mindfulness session.")
        
        _ , mid, _ = st.columns([2, 1, 2])
        
        with mid:
            if st.button("Start"):
                st.session_state.mindfulness_stage = "eyes_closed"
                st.rerun()
                go_to_next_page()
                
    elif st.session_state.mindfulness_stage == "eyes_closed":
        st.markdown("### Close your eyes and relax for 30 seconds...")
        with st.empty():
            time.sleep(30)
        st.session_state.mindfulness_stage = "eyes_open"
        st.rerun()

    # Stage 2: Eyes open with fixation cross
    elif st.session_state.mindfulness_stage == "eyes_open":
        st.markdown("### Open your eyes and focus on the '+' sign for 30 seconds.")
        st.markdown("<h1 style='text-align: center; font-size: 100px;'>+</h1>", unsafe_allow_html=True)
        time.sleep(30)
        st.session_state.mindfulness_stage = "dot_activity"
        st.rerun()

    # Stage 3: Ball moving (your existing dot activity)
    elif st.session_state.mindfulness_stage == "dot_activity":
        st.markdown("### Follow the moving ball on the screen for 30 seconds.")

        # Simple placeholder animation using markdown
        placeholder = st.empty()
        cols = 5

        for i in range(10):
            position = i % cols
            line = ["&nbsp;"] * cols
            line[position] = "🔴"
            placeholder.markdown("<pre style='font-size:30px; text-align:center'>" + "".join(line) + "</pre>", unsafe_allow_html=True)
            time.sleep(30)

        st.session_state.mindfulness_stage = "done"
        st.rerun()

    # Completion
    elif st.session_state.mindfulness_stage == "done":
        st.success("Mindfulness session complete!")
        if st.button("Continue"):
            go_to_next_page()
            st.rerun()
