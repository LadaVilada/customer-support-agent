from typing import List, Dict, Tuple
from .matcher import find_best_match
from .llm_client import LLMClient, LLMError
from .qa_data import qa_data
from .utils import logger


class Chatbot:
    """
    Customer support chatbot for Thoughtful AI.
    Matches user questions to FAQ, falls back to LLM if needed.
    """
    def __init__(self, llm_client: LLMClient):
        """
        Initialize the chatbot with a given LLM client.
        Args:
            llm_client: An instance of LLMClient (dependency injection).
        """
        self.llm_client = llm_client
        self.qa_data = qa_data

    def get_response(self, user_input: str) -> str:
        """
        Get a response to the user's question.
        Args:
            user_input: The user's question as a string.
        Returns:
            The chatbot's reply as a string.
        """
        answer, score = find_best_match(user_input, self.qa_data)
        if answer:
            return answer
        try:
            return self.llm_client.get_response(user_input)
        except LLMError as e:
            # Log error and show fallback message
            logger.error(f"LLMError: {e}")
            return "Sorry, I couldn’t process your request right now."
        except Exception as e:
            logger.exception("Unexpected error in LLM client.")
            return "Sorry, something went wrong with the AI service."