import streamlit as st
from utils2 import chat


def main():
    st.write("""
    # Image Generator
""")

    message = st.text_area("What do you want to see?",
                           placeholder='Describe your image')

    if st.button("Generate"):
        response = chat(message)
        if isinstance(response, str):
            st.write(response)

        else:
            st.image(response[0], use_container_width=True,
                     caption=response[1])


main()
