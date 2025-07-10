import os
from typing import Dict, Optional
import openai
from openai import OpenAI
from openai import APIError, RateLimitError, OpenAIError

_llm_cache: Dict[str, str] = {}

from dotenv import load_dotenv
load_dotenv()

class LLMError(Exception):
    pass

def get_llm_response(prompt: str, api_key: Optional[str] = None) -> str:
    """
    Get a response from OpenAI's chat model. Uses cache for repeated prompts.
    Args:
        prompt: The user input string.
        api_key: Optionally override the API key (default: from env var OPENAI_API_KEY)
    Returns:
        The chatbot reply as a clean string.
    Raises:
        LLMError: If API key is missing or OpenAI API call fails.
    """
    if prompt in _llm_cache:
        return _llm_cache[prompt]
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMError("OPENAI_API_KEY environment variable not set and no API key provided.")
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        _llm_cache[prompt] = answer
        return answer
    except RateLimitError as e:
        raise LLMError(f"OpenAI Rate Limit Error: {e}")
    except APIError as e:
        raise LLMError(f"OpenAI API Error: {e}")
    except OpenAIError as e:
        raise LLMError(f"OpenAI Error: {e}")
    except Exception as e:
        raise LLMError(f"Unexpected error: {e}") 