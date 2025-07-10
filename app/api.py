from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from .chatbot import Chatbot
from .llm_client import LLMClient
from .utils import log_request

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class HealthResponse(BaseModel):
    status: str
    message: str

app = FastAPI(
    title="Thoughtful AI Customer Support Agent API",
    description="Backend API for the customer support chatbot",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
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

@app.get("/health", response_model=HealthResponse)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "message": "API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> Dict[str, str]:
    """
    Chat endpoint for user messages.
    
    Args:
        request: ChatRequest containing the user's message
        
    Returns:
        ChatResponse containing the bot's response
        
    Raises:
        HTTPException: If the message is empty or processing fails
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        response = chatbot.get_response(request.message.strip())
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Thoughtful AI Customer Support Agent API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    } 