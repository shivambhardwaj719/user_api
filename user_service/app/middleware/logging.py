import logging
import json
from pathlib import Path
from logging.handlers import RotatingFileHandler
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

class APILoggerMiddleware(BaseHTTPMiddleware):
    def _get_logger(self, path: str):
        safe_path = path.strip("/").replace("/", "_") or "root"
        logger_name = f"logs/{safe_path}.log"
        logger = logging.getLogger(logger_name)

        if not logger.handlers:
            handler = RotatingFileHandler(
                logger_name,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8"
            )
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False
            
        return logger

    async def dispatch(self, request: Request, call_next):
        logger = self._get_logger(request.url.path)
        client_ip = request.client.host if request.client else "unknown"

        try:
            response = await call_next(request)
            
            log_entry = {
                "client_ip": client_ip,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
            }
            logger.info("RESPONSE:\n" + json.dumps(log_entry, indent=2))
            return response
            
        except Exception as e:
            error_entry = {
                "client_ip": client_ip,
                "method": request.method,
                "path": request.url.path,
                "exception": str(e),
            }
            logger.error("EXCEPTION:\n" + json.dumps(error_entry, indent=2), exc_info=True)
            raise e
