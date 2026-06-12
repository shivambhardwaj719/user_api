import time
import uuid
import hashlib
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.response.handlers import ResponseHandler
from app.utils.response.messages import ResponseMessages

class InMemoryCache:
    _instance = None
    _cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self, key, default=None):
        item = self._cache.get(key)
        if item is None:
            return default
        value, expiry = item
        if expiry and time.time() > expiry:
            del self._cache[key]
            return default
        return value

    def set(self, key, value, timeout=None):
        expiry = time.time() + timeout if timeout else None
        self._cache[key] = (value, expiry)

    def delete(self, key):
        if key in self._cache:
            del self._cache[key]

class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    DEFAULT_RATE_LIMITS = {
        'GET': {'limit': 15, 'period': 1},
        'POST': {'limit': 10, 'period': 5},
        'PUT': {'limit': 10, 'period': 5},
        'PATCH': {'limit': 10, 'period': 5},
        'DELETE': {'limit': 10, 'period': 5},
    }

    def __init__(self, app):
        super().__init__(app)
        self.cache = InMemoryCache()

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not path.startswith('/api/v1/'):
            return await call_next(request)

        client_ip = request.client.host if request.client else "127.0.0.1"
        method = request.method
        
        config = self.DEFAULT_RATE_LIMITS.get(method, self.DEFAULT_RATE_LIMITS['GET'])
        endpoint_key = f"{path}:{method}"
        
        ip_rate_limit_key = f"rate_limit:ip:{client_ip}:{endpoint_key}"

        if self._is_rate_limited(ip_rate_limit_key, config):
            return ResponseHandler.bad_request(message=ResponseMessages.TOO_MANY_REQUESTS)

        self._record_request(ip_rate_limit_key, config)

        response = await call_next(request)
        return response

    def _is_rate_limited(self, cache_key, rate_config):
        block_key = f"{cache_key}:blocked"
        if self.cache.get(block_key):
            return True

        request_data = self.cache.get(cache_key, [])
        now_ts = time.time()
        recent_requests = [t for t in request_data if t > now_ts - rate_config['period']]

        if len(recent_requests) >= rate_config['limit']:
            self.cache.set(block_key, True, 3 * 60)
            self.cache.delete(cache_key)
            return True

        return False

    def _record_request(self, cache_key, rate_config):
        request_data = self.cache.get(cache_key, [])
        now_ts = time.time()
        recent_requests = [t for t in request_data if t > now_ts - rate_config['period']]
        recent_requests.append(now_ts)
        self.cache.set(cache_key, recent_requests, 3600)
