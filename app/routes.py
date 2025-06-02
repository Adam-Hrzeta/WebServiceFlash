from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth_controller import registro, login

# Blueprints
api_bp = Blueprint('api', __name__)

# Rutas de autenticación
api_bp.route('/registro', methods=['POST'])(registro)
api_bp.route('/login', methods=['POST'])(login)

@api_bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "success",
        "mensaje": "API funcionando correctamente",
        "endpoints": {
            "registro": "/registro",
            "login": "/login",
            "protegido": "/protegido",
        }
    })

@api_bp.route("/protegido", methods=["GET"])
@jwt_required()
def protegido():
    usuario = get_jwt_identity()
    return jsonify({
        "status": "success",
        "mensaje": f"Hola {usuario['correo']}, accediste a una ruta protegida",
        "usuario": usuario
    }), 200