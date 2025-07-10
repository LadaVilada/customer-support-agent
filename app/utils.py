import logging
from fastapi import Request

logger = logging.getLogger("customer_support_agent")

async def log_request(request: Request):
    """
    Log incoming HTTP requests for debugging and monitoring.
    Args:
        request: FastAPI Request object.
    """
    logger.info(f"{request.method} {request.url}") 