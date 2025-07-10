from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .chatbot import Chatbot
from .llm_client import LLMClient
from .utils import log_request

app = FastAPI(title="Thoughtful AI Customer Support Agent API")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection: create chatbot instance
llm_client = LLMClient()
chatbot = Chatbot(llm_client)

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    """
    Middleware to log all incoming requests.
    """
    await log_request(request)
    response = await call_next(request)
    return response

@app.post("/chat")
async def chat_endpoint(payload: dict) -> dict:
    """
    Chat endpoint for user messages.
    Args:
        payload: JSON with {"message": str}
    Returns:
        JSON with {"response": str}
    """
    user_message = payload.get("message", "")
    response = chatbot.get_response(user_message)
    return {"response": response} 