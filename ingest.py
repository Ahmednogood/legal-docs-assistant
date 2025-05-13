import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
from qdrant_client import QdrantClient
from langchain.chat_models import ChatOpenAI

load_dotenv()

# Load documents from multiple formats
loaders = [
    DirectoryLoader("data", glob="**/*.txt", loader_cls=TextLoader),
    DirectoryLoader("data", glob="**/*.pdf", loader_cls=PyPDFLoader),
    DirectoryLoader("data", glob="**/*.docx", loader_cls=UnstructuredWordDocumentLoader),
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# Generate a summary using the first few chunks
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
joined_text = "\n\n".join([doc.page_content for doc in splits[:5]])
summary_prompt = f"Summarize this legal document in plain English:\n\n{joined_text}"
summary = llm.predict(summary_prompt)

print("\n📄 Plain English Summary:\n")
print(summary)

# Embed and store in Qdrant
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
Qdrant.from_documents(
    documents=splits,
    embedding=embedding,
    path="qdrant_data",
    collection_name="legal_docs"
)

print("\n✅ Ingestion and embedding complete.")
