from langchain_groq import ChatGroq
from app.config.config import config
from app.common.loggers import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

GROQ_API_KEY  = config.GROQ_API_KEY
MODEL_NAME = config.MODEL_NAME

def load_llm(model_name: str = MODEL_NAME, groq_api_key: str = GROQ_API_KEY):
    try:
        logger.info("Loading LLM from Groq using LLaMA3 model...")

        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=0.3,
            max_tokens=256,
            streaming=True
        )

        logger.info("LLM loaded successfully from Groq.")
        return llm

    except Exception as e:
        error_message = CustomException("Failed to load an LLM from Groq", e)
        logger.error(str(error_message))
        return None