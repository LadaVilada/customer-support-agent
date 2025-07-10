import pytest
from app.chatbot import Chatbot
from app.llm_client import LLMClient

class MockLLMClient:
    def __init__(self, reply: str = "LLM fallback reply"):
        self.reply = reply
        self.calls = []
    def get_response(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self.reply

def test_faq_match():
    chatbot = Chatbot(llm_client=MockLLMClient())
    # Should match FAQ exactly
    response = chatbot.get_response("What does the claims processing agent (CAM) do?")
    assert "CAM streamlines the submission" in response

def test_llm_fallback():
    chatbot = Chatbot(llm_client=MockLLMClient("LLM fallback"))
    # Should fallback to LLM for unrelated question
    response = chatbot.get_response("How do I reset my password?")
    assert response == "LLM fallback"

def test_llm_error():
    class ErrorLLMClient:
        def get_response(self, prompt: str) -> str:
            raise Exception("LLM is down!")
    chatbot = Chatbot(llm_client=ErrorLLMClient())
    response = chatbot.get_response("Unmatched question")
    assert "LLM Error" in response 