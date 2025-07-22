import streamlit as st
import time
import random

def render(go_to_next_page):
    # Initialize the main stage controller if it doesn't exist
    if "activity_stage" not in st.session_state:
        st.session_state.activity_stage = "eyes_closed"
        
    if st.session_state.activity_stage == "eyes_closed":
        st.subheader("Activity 1: Eyes Closed")
        st.write("Focus on your breath and stay still for 30 seconds. A gentle sound will indicate the end. Press the button below to start.")

        if "eyes_closed_started" not in st.session_state:
            if st.button("Begin Eyes Closed Activity"):
                st.session_state.eyes_closed_started = True
                st.session_state.eyes_closed_timer_start = time.time()
                st.rerun()
        else:
            elapsed = time.time() - st.session_state.eyes_closed_timer_start
            remaining = int(30 - elapsed)

            if remaining > 0:
                st.write(f"⏳ Time left: **{remaining} seconds**")
                time.sleep(1) # This creates the 1-second refresh loop
                st.rerun()
            else:
                st.success("✅ Eyes Closed activity complete!")
                # Sound will be blocked by browsers, but st.audio provides a manual player
                st.audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg", autoplay=True)
                
            
                if st.button("Continue to next activity"):
                    st.session_state.activity_stage = "fixation_cross"
                    # Clean up old state variables before moving on
                    del st.session_state.eyes_closed_started
                    del st.session_state.eyes_closed_timer_start
                    st.rerun()


    elif st.session_state.activity_stage == "fixation_cross":
        st.subheader("Activity 2: Fixation Cross")
        st.write("Now please focus on the '+' sign for 30 seconds.")

        if "fixation_cross_started" not in st.session_state:
            if st.button("Begin Fixation Cross Activity"):
                st.session_state.fixation_cross_started = True
                st.session_state.fixation_cross_timer_start = time.time()
                st.rerun()
        else:
            st.markdown("<h1 style='text-align: center; font-size: 100px;'>+</h1>", unsafe_allow_html=True)
            elapsed = time.time() - st.session_state.fixation_cross_timer_start
            remaining = int(30 - elapsed)

            if remaining > 0:
                #st.write(f"⏳ Time left: **{remaining} seconds**")
                time.sleep(1)
                st.rerun()
            else:
                st.success("✅ Fixation Cross activity complete!")
                if st.button("Continue to Dot Activity"):
                    st.session_state.activity_stage = "dot_activity"
                    # Clean up old state variables
                    del st.session_state.fixation_cross_started
                    del st.session_state.fixation_cross_timer_start
                    st.rerun()
                    
                    
    elif st.session_state.activity_stage == "dot_activity":
        st.subheader("Activity 3: Dot Activity")
        st.write("Follow the dot with your eyes and **click it when it turns red.**")

        if "dot_activity_started" not in st.session_state:
            if st.button("Start Dot Activity"):
                st.session_state.dot_activity_started = True
                st.session_state.dot_activity_timer_start = time.time()
                st.rerun()
        else:
            elapsed_time = time.time() - st.session_state.dot_activity_timer_start
            remaining = int(30 - elapsed_time)
            st.write(f"⏳ Time left: **{remaining} seconds**")

            # Initialize dot properties if they don't exist
            if "dot_color" not in st.session_state:
                st.session_state.dot_color = "blue"
                st.session_state.dot_x = random.randint(10, 90)
                st.session_state.dot_y = random.randint(20, 80) # Adjusted Y to be less likely to overlap text
                st.session_state.dot_last_update = time.time()

            # Update dot position and color periodically
            if time.time() - st.session_state.dot_last_update > 1.5:
                st.session_state.dot_color = random.choice(["blue", "red"])
                st.session_state.dot_x = random.randint(10, 90)
                st.session_state.dot_y = random.randint(20, 80)
                st.session_state.dot_last_update = time.time()

            dot_html = f"""
            <div style="position: relative; height: 300px; border: 1px solid #ddd; border-radius: 5px;">
                <span style="
                    position: absolute;
                    left: {st.session_state.dot_x}%;
                    top: {st.session_state.dot_y}%;
                    width: 30px;
                    height: 30px;
                    background-color: {st.session_state.dot_color};
                    border-radius: 50%;
                    transform: translate(-50%, -50%);
                "></span>
            </div>
            """
            st.markdown(dot_html, unsafe_allow_html=True)

            if remaining > 0:
                time.sleep(1)
                st.rerun()
            else:
                st.success("✅ Dot activity complete!")
                if st.button("Proceed to Stories"):
                    go_to_next_page()
                    st.rerun()