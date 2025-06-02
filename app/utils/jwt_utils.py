from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Token inválido o expirado',
                'mensaje': str(e)
            }), 401
    return decorated

def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña usando PBKDF2 con SHA256"""
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(hash_password: str, password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return check_password_hash(hash_password, password)

def create_token_payload(user_id: int, email: str, role: str = 'negocio'):
    """Crea el payload para el token JWT"""
    return {
        'user_id': user_id,
        'email': email,
        'role': role
    } 