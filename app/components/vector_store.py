from app.components.embeddings import get_embedding_model
from app.config.config import config
from app.common.custom_exception import CustomException
from app.common.loggers import get_logger
from langchain_community.vectorstores import FAISS
import os

DB_PATH = config.DB_FAISS_PATH
logger = get_logger(__name__)

def load_vector_store():
    try:
        embedding_model = get_embedding_model()
        if os.path.exists(DB_PATH):
            logger.info("Try to load previous vector store")
            return FAISS.load_local(
                DB_PATH,
                embedding_model,
                allow_dangerous_deserialization = True
            )
        else:
            logger.warning("DB Does not exist")
    except Exception as e:
        error_message = CustomException("Failed to load existing vector DB",e)
        logger.error(error_message)
        raise error_message

def create_vector_store(text):
    try:
        if not text:
            raise CustomException("No chunks were found")
        logger.info("Generating New Vectorstore")
        embedding_model = get_embedding_model()
        db = FAISS.from_documents(text, embedding_model)
        logger.info("Vector DB Created")
        db.save_local(DB_PATH)
        logger.info("Vector loaded succesfully")
        return db
    except Exception as e:
        error_message = CustomException("Failed to  create Vector DB",e)
        logger.error(error_message)
        raise error_message



if __name__ == "__main__":
    load_vector_store()
    create_vector_store(text=None)