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

def test_health_endpoint():
    """Test the health check endpoint."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "message" in data

def test_root_endpoint():
    """Test the root endpoint."""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data
    assert "endpoints" in data

def test_chat_faq():
    """Test chat endpoint with FAQ question."""
    resp = client.post("/chat", json={"message": "What does the claims processing agent (CAM) do?"})
    assert resp.status_code == 200
    assert "CAM streamlines the submission" in resp.json()["response"]

def test_chat_llm_fallback():
    """Test chat endpoint with non-FAQ question (should use LLM fallback)."""
    resp = client.post("/chat", json={"message": "How do I reset my password?"})
    assert resp.status_code == 200
    assert "feel free to reach out to our support" in resp.json()["response"]

def test_chat_empty_message():
    """Test chat endpoint with empty message."""
    resp = client.post("/chat", json={"message": ""})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"]

def test_chat_whitespace_message():
    """Test chat endpoint with whitespace-only message."""
    resp = client.post("/chat", json={"message": "   "})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"]