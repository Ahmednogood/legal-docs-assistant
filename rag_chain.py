import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from qdrant_client import QdrantClient

load_dotenv()

qdrant = QdrantClient(path="qdrant_data")

embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Qdrant(
    client=qdrant,
    collection_name="legal_docs",
    embeddings=embedding
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
