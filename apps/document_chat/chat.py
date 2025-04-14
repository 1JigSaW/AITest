import time
import streamlit as st
from apps.document_chat.helper import DocumentIngestorHelper


class DocumentChatApp:
    """
    Searching local docs.
    """
    def __init__(
            self,
            data_folder: str = "data",
            db_path: str = "./chroma_db",
    ):
        self.title = "Document Chat"
        self.description = "Search local docs (RAG) with Chroma and display results incrementally."
        self.ingestor = DocumentIngestorHelper(
            data_folder=data_folder,
            persist_directory=db_path,
        )

    def run(self):
        st.title(self.title)
        st.write(self.description)

        user_input = st.text_input("Input:", value="")
        if st.button("Send"):
            if user_input.strip():
                try:
                    vectorstore = self.ingestor.load_vectorstore()
                    docs = vectorstore.similarity_search(user_input, k=1)
                except Exception as e:
                    st.error(f"Error during document search: {str(e)}")
                    return

                st.write("**Your input:**", user_input)
                st.write("**Response:**")
                if docs:
                    for i, doc in enumerate(docs, start=1):
                        st.markdown(f"**Document {i} (source: {doc.metadata['source']}):**")
                        output_container = st.empty()
                        full_text = doc.page_content
                        sentences = full_text.split('. ')
                        accumulated = ""
                        try:
                            for sentence in sentences:
                                if sentence.strip():
                                    accumulated += sentence.strip() + ". "
                                    output_container.markdown(accumulated)
                                    time.sleep(0.3)
                        except Exception as e:
                            st.error(f"Error during streaming output: {str(e)}")
                            output_container.text("Streaming interrupted due to error.")
                else:
                    st.write("No relevant documents found.")
            else:
                st.info("Please enter a valid input.")