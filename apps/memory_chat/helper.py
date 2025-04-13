import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from streming import StreamlitStreamingCallback


class MemoryChatHelper:
    """
    Encapsulates the logic for a memory-based chat with streaming output.
    """

    def __init__(self):

        self.llm_model = "gpt-4o"
        self.temperature = 0.0

        if "chat_memory" not in st.session_state:
            st.session_state.chat_memory = ConversationBufferMemory(
                return_messages=True,
            )
        self.memory = st.session_state.chat_memory

    def invoke_streaming(
            self,
            user_message: str,
            output_container: st.delta_generator.DeltaGenerator,
    ) -> str:
        """
        Invokes the conversation chain in streaming mode.
        """

        streaming_callback = StreamlitStreamingCallback(output_container)


        streaming_llm = ChatOpenAI(
            model_name=self.llm_model,
            temperature=self.temperature,
            streaming=True,
            callbacks=[streaming_callback]
        )


        streaming_chain = ConversationChain(
            llm=streaming_llm,
            memory=self.memory,
        )
        try:
            final_response = streaming_chain.run(user_message)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            final_response = "Fallback response: Sorry, something went wrong."
        return final_response