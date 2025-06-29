import streamlit as st
import time
import random

def render(go_to_next_page):
    if "activity_stage" not in st.session_state:
        st.session_state.activity_stage = "eyes_closed"

    if st.session_state.activity_stage == "eyes_closed":
        st.subheader("Close your eyes for 1 minute")
        st.write("Focus on your breath and stay still. A gentle sound will indicate the end.")

        if "eyes_closed_started" not in st.session_state:
            if st.button("Start Meditation"):
                st.session_state.eyes_closed_started = True
                st.session_state.timer_start = time.time()
                st.rerun()
        else:
            elapsed = time.time() - st.session_state.timer_start
            remaining = int(2 - elapsed)

            if remaining > 0:
                st.write(f"⏳ Time left: **{remaining} seconds**")
                time.sleep(1)
                st.rerun()
            else:
                st.success("✅ 1 minute completed!")
                st.markdown(
                    """
                    <audio autoplay>
                        <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
                    </audio>
                    """, unsafe_allow_html=True
                )
                if st.button("Continue to Next Activity"):
                    st.session_state.activity_stage = "eyes_open"
                    st.session_state.activity_start_time = time.time()
                    st.rerun()

    elif st.session_state.activity_stage == "eyes_open":
        st.subheader("Eyes Open Activity")
        st.write("Follow the dot with your eyes and **click it when it turns red.**")

        if "eyes_open_started" not in st.session_state:
            if st.button("Start Dot Activity"):
                st.session_state.eyes_open_started = True
                st.session_state.activity_start_time = time.time()
                st.rerun()
        else:
            elapsed_time = time.time() - st.session_state.activity_start_time
            remaining = int(5 - elapsed_time)
            st.write(f"⏳ Time left: **{remaining} seconds**")

            if "dot_color" not in st.session_state:
                st.session_state.dot_color = "blue"
                st.session_state.dot_x = random.randint(10, 90)
                st.session_state.dot_y = random.randint(10, 90)
                st.session_state.dot_last_update = time.time()

            if time.time() - st.session_state.dot_last_update > 1.5:
                st.session_state.dot_color = random.choice(["blue", "red"])
                st.session_state.dot_x = random.randint(10, 90)
                st.session_state.dot_y = random.randint(10, 90)
                st.session_state.dot_last_update = time.time()

            dot_html = f"""
            <style>
            .dot-btn {{
                position: absolute;
                left: {st.session_state.dot_x}%;
                top: {st.session_state.dot_y}%;
                transform: translate(-50%, -50%);
                background-color: {st.session_state.dot_color};
                border: none;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                cursor: pointer;
                z-index: 9999;
            }}
            </style>
            <button class="dot-btn"></button>
            """
            st.markdown(dot_html, unsafe_allow_html=True)

            if remaining > 0:
                time.sleep(1)
                st.rerun()
            else:
                st.success("✅ Dot activity complete!")
                if st.button("Proceed to Quiz"):
                    st.session_state.activity_stage = None
                    go_to_next_page()
                    st.rerun()
