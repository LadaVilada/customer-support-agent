import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.chatbot import Chatbot
from app.llm_client import LLMClient

# Patch the chatbot in the app to use a mock LLMClient
def setup_module(module):
    class MockLLMClient:
        def get_response(self, prompt):
            return "Mocked LLM reply"
    app.dependency_overrides = {}
    app.chatbot = Chatbot(MockLLMClient())

client = TestClient(app)

def test_chat_faq():
    resp = client.post("/chat", json={"message": "What does the claims processing agent (CAM) do?"})
    assert resp.status_code == 200
    assert "CAM streamlines the submission" in resp.json()["response"]

def test_chat_llm_fallback():
    resp = client.post("/chat", json={"message": "How do I reset my password?"})
    assert resp.status_code == 200
    assert resp.json()["response"] == "Mocked LLM reply" 