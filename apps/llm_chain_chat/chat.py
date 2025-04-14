import streamlit as st
import dotenv

from apps.llm_chain_chat.helper import LLMChainHelper

dotenv.load_dotenv()


class LLMChainChatApp:
    """
    LLM Chain chat app.
    """

    def __init__(self):
        self.title = "LLM Chain Chat"
        self.description = (
            "This demo uses a PromptTemplate + LLMChain with streaming output. "
            "Your query is processed and the response is delivered incrementally."
        )
        self.logic = LLMChainHelper()

    def run(self):
        st.title(self.title)
        st.write(self.description)

        user_query = st.text_input("Your query for the LLM:", value="")
        if st.button("Send"):
            if user_query.strip():

                output_container = st.empty()
                output_container.text("")

                final_response = self.logic.invoke_streaming(user_query, output_container)
                st.write("**Final Response:**", final_response)
            else:
                st.info("Please enter a query.")
