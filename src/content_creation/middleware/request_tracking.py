from fastapi import Request
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_host": request.client.host if request.client else None
            }
        )
        
        try:
            response = await call_next(request)
            
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code
                }
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "error": str(e)
                }
            )
            raise
