from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    def is_rate_limited(self, ip):
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Limpiar solicitudes antiguas
        self.requests[ip] = [req_time for req_time in self.requests[ip] 
                           if req_time > minute_ago]
        
        # Verificar si excede el límite
        if len(self.requests[ip]) >= self.requests_per_minute:
            return True
        
        # Agregar nueva solicitud
        self.requests[ip].append(now)
        return False

rate_limiter = RateLimiter()

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        if rate_limiter.is_rate_limited(ip):
            return jsonify({
                'error': 'Too many requests',
                'message': 'Please try again later'
            }), 429
        return f(*args, **kwargs)
    return decorated_function 