import streamlit as st
import dotenv

from apps.memory_chat.helper import MemoryChatHelper

dotenv.load_dotenv()

class MemoryChatApp:
    """
    MemoryChatApp provides a simple Streamlit UI for the memory chat.
    """
    def __init__(self):
        self.title = "Memory Chat"
        self.description = (
            "This demo maintains conversation context across multiple turns. Your previous messages are remembered, "
            "so the LLM can generate context-aware replies. The response output is streamed incrementally."
        )
        self.logic = MemoryChatHelper()

    def run(self):
        st.title(self.title)
        st.write(self.description)
        user_message = st.text_input("You:", value="")
        if st.button("Send (Memory Chat with Streaming)"):
            if user_message.strip():
                output_container = st.empty()
                output_container.text("")
                final_response = self.logic.invoke_streaming(user_message, output_container)
                st.write("**Final Response:**", final_response)
            else:
                st.info("Please enter a message.")
