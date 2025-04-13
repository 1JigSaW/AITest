import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma

class DocumentIngestorHelper:
    """
    Loads, splits documents, and stores them in a local Chroma vector DB.
    Also provides methods to load the vector store for querying.
    """
    def __init__(self, data_folder: str, persist_directory: str = "./chroma_db", collection_name: str = "my_documents"):
        self.data_folder = data_folder
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

    def ingest(self):
        """
        Loads files from data_folder, splits them, creates embeddings,
        and persists them to a local Chroma DB.
        """
        docs = []
        for file_name in os.listdir(self.data_folder):
            if file_name.endswith((".txt", ".md")):
                with open(os.path.join(self.data_folder, file_name), "r", encoding="utf-8") as f:
                    text = f.read()
                docs.append(Document(page_content=text, metadata={"source": file_name}))

        splitted_docs = []
        for doc in docs:
            chunks = self.text_splitter.split_text(doc.page_content)
            for chunk in chunks:
                splitted_docs.append(Document(page_content=chunk, metadata=doc.metadata))

        self.vectorstore = Chroma.from_documents(
            splitted_docs,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory
        )
        self.vectorstore.persist()

    def load_vectorstore(self):
        """
        Loads the existing Chroma vector store from disk (or returns a cached version).
        """
        if self.vectorstore is None:
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )
        return self.vectorstore
