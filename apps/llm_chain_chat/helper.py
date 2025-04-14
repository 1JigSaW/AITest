from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import streamlit as st


from apps.llm_chain_chat.prompt import PROMPT_TEMPLATE
from streming import StreamlitStreamingCallback


class LLMChainHelper:
    """
    LLM Chain Helper.
    """

    def __init__(self):
        self.prompt = PromptTemplate(
            input_variables=["user_query"],
            template=PROMPT_TEMPLATE
        )

    def invoke_streaming(
            self,
            user_query: str,
            output_container: st.delta_generator.DeltaGenerator,
    ) -> str:
        """
        Invokes the LLM chain in streaming mode.
        """

        streaming_callback = StreamlitStreamingCallback(
            output_container,
        )

        streaming_llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.0,
            streaming=True,
            callbacks=[streaming_callback]
        )


        streaming_chain = LLMChain(
            llm=streaming_llm,
            prompt=self.prompt
        )

        try:
            final_response = streaming_chain.run({"user_query": user_query})
        except Exception as e:
            st.error(f"Error during LLM call: {str(e)}")
            final_response = "Fallback response: Sorry, something went wrong."

        return final_response
