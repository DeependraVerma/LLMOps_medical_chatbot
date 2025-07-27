import os
from app.common.loggers import get_logger
from app.common.custom_exception import CustomException
from app.components.pdf_loader import load_pdf_files,create_text_chunks
from app.components.vector_store import create_vector_store
from app.config.config import config

logger = get_logger(__name__)



def process_vectorisation():
    try:
        data = load_pdf_files()
        documents =  create_text_chunks(documents=data)
        logger.info("Documents Created")
        vector_db = create_vector_store(text=documents)
        logger.info("Created Vector DB")
    except Exception as e:
        error_message = CustomException(f"Failed to process Vectorisation - {str(e)}")
        logger.error(error_message)
        raise error_message



if __name__ == "__main__":
    process_vectorisation()