from langchain_huggingface import HuggingFaceEmbeddings

from app.common.custom_exception import CustomException
from app.common.loggers import get_logger

logger = get_logger(__name__)


def get_embedding_model():
    try:
        logger.info("Initializing our Huggingface embedding")
        model = HuggingFaceEmbeddings(model_name = "BAAI/bge-small-en")
        logger.info("Huggingface embedding model loaded succesfully")
        return model
    except Exception as e:
        logger.error(f"Unable to load model - {str(e)}")
        raise CustomException("Unable to load model", str(e))



if __name__ == "__main__":
    print(get_embedding_model())