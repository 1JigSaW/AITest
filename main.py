import streamlit as st
import dotenv

from apps.document_chat.chat import DocumentChatApp
from apps.document_chat.helper import DocumentIngestorHelper
from apps.flow_chat.chat import FlowChatApp
from apps.llm_chain_chat.chat import LLMChainChatApp
from apps.memory_chat.chat import MemoryChatApp

dotenv.load_dotenv()



def main():
    doc_chat_app = DocumentChatApp()
    llm_chain_chat_app = LLMChainChatApp()
    flow_chat_app = FlowChatApp()
    memory_chat_app = MemoryChatApp()

    st.sidebar.title("Select Chat Mode")

    chat_mode = st.sidebar.radio(
        "Choose a chat mode:",
        (
            "Document Chat",
            "LLM Chain Chat",
            "LangGraph Flow Chat",
            "Memory Chat",
        )
    )

    if chat_mode == "Document Chat":
        doc_chat_app.run()
    elif chat_mode == "LLM Chain Chat":
        llm_chain_chat_app.run()
    elif chat_mode == "LangGraph Flow Chat":
        flow_chat_app.run()
    elif chat_mode == "Memory Chat":
        memory_chat_app.run()


if __name__ == "__main__":
    ingestor = DocumentIngestorHelper(
        data_folder="data",
        persist_directory="./chroma_db",
    )
    ingestor.ingest()
    main()