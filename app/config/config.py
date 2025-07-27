import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = "llama-3.1-8b-instant"
    DB_FAISS_PATH = "vectorstore/db_faiss"
    DATA_PATH = "data/"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50


config = Config()
