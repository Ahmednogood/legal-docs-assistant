import os
import chainlit as cl
from dotenv import load_dotenv
import logging

# Fix for Hugging Face permission error
os.environ["CHAINLIT_FILES_DIR"] = "/tmp/chainlit_files"
os.makedirs("/tmp/chainlit_files", exist_ok=True)

from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.chains import RetrievalQA
from qdrant_client import QdrantClient
from langchain.prompts import PromptTemplate

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env variables
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing in .env")

@cl.on_chat_start
async def on_chat_start():
    try:
        await cl.Message(content="📄 Please upload a legal document (.pdf, .docx, or .txt) to begin.").send()

        files = await cl.AskFileMessage(
            content="📎 Upload Legal Document",
            accept=[".pdf", ".txt", ".docx"],
            max_size_mb=10
        ).send()

        if not files:
            await cl.Message(content="❌ No file was uploaded.").send()
            return

        file = files[0]
        file_name = file.name.lower()
        temp_path = file.path

        # Load document
        if file_name.endswith(".pdf"):
            loader = PyPDFLoader(temp_path)
        elif file_name.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(temp_path)
        elif file_name.endswith(".txt"):
            loader = TextLoader(temp_path)
        else:
            await cl.Message(content="❌ Unsupported file type.").send()
            return

        docs = loader.load()
        if not docs:
            await cl.Message(content="❌ Could not extract any text from the file.").send()
            return

        # Chunk documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""]
        )
        chunks = text_splitter.split_documents(docs)

        # Embed & vectorstore
        embedding = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small"
        )

        vectorstore = Qdrant.from_documents(
            documents=chunks,
            embedding=embedding,
            path=":memory:",
            collection_name="legal_docs"
        )

        llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # Prompt template
        prompt_template = """You are a helpful legal document assistant. Answer questions about the provided legal document in a clear and concise manner. 
If the information is not in the document, simply say "I don't have enough information to answer that question."
If you're not sure about something, say so.
Keep your answers brief and to the point.

Context: {context}
Question: {question}
Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # Configure QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(
                search_kwargs={
                    "k": 6,
                    "score_threshold": 0.3
                }
            ),
            return_source_documents=False,
            chain_type="stuff",
            chain_type_kwargs={"prompt": PROMPT}
        )

        cl.user_session.set("qa_chain", qa_chain)
        await cl.Message(content="✅ Document processed! Ask your legal questions below.").send()

    except Exception as e:
        logger.error(f"Error during chat start: {e}")
        await cl.Message(content=f"❌ An error occurred: {str(e)}").send()

@cl.on_message
async def on_message(message: cl.Message):
    try:
        qa_chain = cl.user_session.get("qa_chain")
        if not qa_chain:
            await cl.Message(content="⚠️ Please upload a document first.").send()
            return

        response = qa_chain.invoke({"query": message.content})
        await cl.Message(content=response["result"]).send()

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await cl.Message(content=f"❌ Failed to answer: {str(e)}").send()
