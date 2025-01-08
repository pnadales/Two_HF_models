import streamlit as st
from utils import send_message, print_chat, delete_messages


def main():
    st.write("""
    # Chat TPG
""")

    if st.button("Clear memory"):
        delete_messages()
    message = st.text_area("Can I help you?",
                           placeholder='Send a message to the Chat')

    if st.button("Send"):
        st.write(print_chat(send_message(message.strip())))


main()
