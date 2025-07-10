from typing import Optional
from openai import OpenAI, APIError, RateLimitError, OpenAIError
from .config import OPENAI_API_KEY, OPENAI_MODEL, SYSTEM_PROMPT

class LLMError(Exception):
    """Custom exception for LLM errors."""
    pass

class LLMClient:
    """
    Abstraction for a Large Language Model (LLM) client (e.g., OpenAI).
    """
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, system_prompt: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_MODEL
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.client = OpenAI(api_key=self.api_key)
        self._cache = {}

    def get_response(self, prompt: str) -> str:
        """
        Get a response from the LLM, using cache for repeated prompts.
        Args:
            prompt: The user input string.
        Returns:
            The chatbot reply as a clean string.
        Raises:
            LLMError: If API key is missing or OpenAI API call fails.
        """
        if prompt in self._cache:
            return self._cache[prompt]
        if not self.api_key:
            raise LLMError("OPENAI_API_KEY not set.")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0.7,
            )
            answer = response.choices[0].message.content.strip()
            self._cache[prompt] = answer
            return answer
        except RateLimitError as e:
            raise LLMError(f"OpenAI Rate Limit Error: {e}")
        except APIError as e:
            raise LLMError(f"OpenAI API Error: {e}")
        except OpenAIError as e:
            raise LLMError(f"OpenAI Error: {e}")
        except Exception as e:
            raise LLMError(f"Unexpected error: {e}") 