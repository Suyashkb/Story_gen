import streamlit as st
import time
import random
#from pylsl import StreamInfo, StreamOutlet 

def render(go_to_next_page):
    # Initialize the main stage controller if it doesn't exist
    if "activity_stage" not in st.session_state:
        st.session_state.activity_stage = "eyes_closed"
        
    if st.session_state.activity_stage == "eyes_closed":
        st.subheader("Activity 1")
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


    # ADD THIS NEW BLOCK IN ITS PLACE
    elif st.session_state.activity_stage == "fixation_cross":
        # 1. Initialize a specific state for this activity
        if "fixation_stage" not in st.session_state:
            st.session_state.fixation_stage = "instruction"

        # --- INSTRUCTION PHASE ---
        if st.session_state.fixation_stage == "instruction":
            st.subheader("Activity 2")
            st.write("Now please focus on the '+' sign for 30 seconds. To begin the experiment press the button below.")
            if st.button("Begin Fixation Cross Activity"):
                # Set the timer and move to the 'running' stage
                st.session_state.fixation_cross_timer_start = time.time()
                st.session_state.fixation_stage = "running"
                st.rerun()

        # --- RUNNING PHASE ---
        elif st.session_state.fixation_stage == "running":
            elapsed = time.time() - st.session_state.fixation_cross_timer_start
            
            if elapsed < 30:
                # Display ONLY the fixation cross, ensuring no other text is drawn
                st.markdown("""
                    <div style='display: flex; justify-content: center; align-items: center; height: 70vh;'>
                        <p style='text-align: center; font-size: 100px;'>+</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # This loop forces a rerun to check the timer
                time.sleep(1)
                st.rerun()
            else:
                # Once the timer is done, move to the 'finished' stage
                st.session_state.fixation_stage = "finished"
                st.rerun()

        # --- FINISHED PHASE ---
        elif st.session_state.fixation_stage == "finished":
            st.success("✅ Fixation Cross activity complete!")
            if st.button("Continue to Dot Activity"):
                # Move to the next main activity
                st.session_state.activity_stage = "dot_activity"
                # Clean up the state variables for this activity
                del st.session_state.fixation_stage
                del st.session_state.fixation_cross_timer_start
                st.rerun()
                    
    elif st.session_state.activity_stage == "dot_activity":
        st.subheader("Activity 3: Eye Movement Task")
        st.write("Please follow the dot with your eyes as it moves from left to right.")

        # This block runs BEFORE the activity starts
        if "dot_activity_started" not in st.session_state:
            if st.button("Start Eye Movement Activity"):
                st.session_state.dot_activity_started = True
                st.session_state.dot_activity_timer_start = time.time() # Main timer for the activity
                st.session_state.sweep_start_time = time.time()         # Timer for the 5-second sweep
                st.rerun()
        else:
            # Check the main timer for the whole activity
            elapsed = time.time() - st.session_state.dot_activity_timer_start
            TOTAL_DURATION = 30  # Set a total duration for the activity

            # This is the DURING phase (timer is still running)
            if elapsed < TOTAL_DURATION:
                remaining_total = int(TOTAL_DURATION - elapsed)
                st.write(f"⏳ Time left: **{remaining_total} seconds**")

                # --- Dot Animation Logic ---
                horizontal_steps = [10, 30, 50, 70, 90, 120, 150]
                SWEEP_DURATION_SECONDS = 3.0
                current_time = time.time()

                if "sweep_start_time" not in st.session_state:
                    st.session_state.sweep_start_time = current_time

                if current_time - st.session_state.sweep_start_time > SWEEP_DURATION_SECONDS:
                    st.session_state.sweep_start_time = current_time

                elapsed_in_sweep = current_time - st.session_state.sweep_start_time
                step_index = int(elapsed_in_sweep)
                step_index = min(step_index, len(horizontal_steps) - 1)
                dot_x_position = horizontal_steps[step_index]

                # VISIBILITY FIX: Increased container height and dot size for better visibility
                dot_html = f"""
                <div style='position: relative; height: 200px; border: 2px solid #666; border-radius: 8px; margin-top: 20px;'>
                    <div style='
                        position: absolute;
                        left: {dot_x_position}%;
                        top: 50%;
                        width: 35px;
                        height: 35px;
                        background-color: black;
                        border-radius: 50%;
                        transform: translate(-50%, -50%);
                        transition: left 0.5s ease-in-out;
                    '></div>
                </div>
                """
                st.markdown(dot_html, unsafe_allow_html=True)

                time.sleep(0.1)
                st.rerun()

            # This is the AFTER phase (timer has finished)
            else:
                st.success("✅ Dot activity complete!")
                if st.button("Proceed to Stories"):
                    # Clean up state variables for this activity
                    del st.session_state.dot_activity_started
                    del st.session_state.dot_activity_timer_start
                    del st.session_state.sweep_start_time
                    go_to_next_page()
                    st.rerun()