import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys

from app.common.loggers import get_logger
from app.common.custom_exception import CustomException

from app.config.config import config


DATA_PATH = config.DATA_PATH
CHUNK_SIZE = config.CHUNK_SIZE
CHUNK_OVERLAP = config.CHUNK_OVERLAP

logger = get_logger(__name__)


def load_pdf_files():
    try:
        if not os.path.exists(DATA_PATH):
            raise CustomException("Data Path Does not exist")
        logger.info(f"Loading files from {DATA_PATH}")
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        if not documents:
            logger.warning(f"No Data in {DATA_PATH}")
        logger.info(f"Documents loaded, number = {len(documents)}")
        return documents
    except Exception as e:
        logger.error(f"Failed to load Data - {e}")
        raise CustomException("Failed to load data", e)


def create_text_chunks(documents):
    try:
        if not documents:
            raise CustomException("No documents found")
        logger.info(f"Changing {len(documents)} into chunks")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = CHUNK_SIZE, chunk_overlap = CHUNK_OVERLAP)

        text_chunks = text_splitter.split_documents(documents)
        logger.info(f"Generated text chunks of length - {len(text_chunks)}")
        return text_chunks
    except Exception as e:
        logger.error(f"Failed to chunk Data - {e}")
        raise CustomException("Failed to chunk data", e)

documents = load_pdf_files()

print(create_text_chunks(documents))
