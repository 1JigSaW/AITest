import time
import streamlit as st

from apps.flow_chat.helper import FlowGraphHelper


class FlowChatApp:
    """
    A minimal Streamlit UI for the Flow Chat.
    All the heavy lifting (graph building, compilation, and invocation) is encapsulated in FlowGraphHelper.
    """
    def __init__(self):
        self.title = "LangGraph Flow Chat"
        self.description = (
            "Enter your message and see the multi-step processing (Think → Act → Branch → Observe). "
            "The response is streamed incrementally."
        )
        self.flow_logic = FlowGraphHelper()

    def run(self):
        st.title(self.title)
        st.write(self.description)
        user_input = st.text_input("Enter your message:")
        if st.button("Send (Flow Chat with Streaming)"):
            if user_input.strip():
                try:

                    final_text = self.flow_logic.invoke_flow(user_input)
                except Exception as e:
                    st.error(f"Error invoking flow: {str(e)}")
                    final_text = "Fallback output: Sorry, something went wrong."

                output_container = st.empty()
                streamed_text = ""
                try:
                    for word in final_text.split():
                        streamed_text += word + " "
                        output_container.markdown(streamed_text)
                        time.sleep(0.2)
                except Exception as e:
                    st.error(f"Error during streaming: {str(e)}")
            else:
                st.info("Please enter a valid input.")
