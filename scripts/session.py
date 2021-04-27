import streamlit as st
import SessionState


def main():
    st.subheader("new")

    session_state = SessionState.get(name="", button_sent=False)

    session_state.name = st.text_input("Enter your name")
    button_sent = st.button("Send")

    if button_sent:
        session_state.button_sent = True

    if session_state.button_sent:
        st.write(session_state.name)

        session_state.bye = st.checkbox("bye")
        session_state.welcome = st.checkbox("welcome")

        if session_state.bye:
            st.write("I see")
        if session_state.welcome:
            st.write("you see")


main()