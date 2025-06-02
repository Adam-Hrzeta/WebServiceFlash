# app/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import login_usuario

# Definir los blueprints
auth_bp = Blueprint('auth', __name__)
negocio_bp = Blueprint('negocio', __name__)

@auth_bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "success",
        "mensaje": "API funcionando correctamente",
        "endpoints": {
            "login": "/api/auth/login",
            "protegido": "/api/auth/protegido",
            "negocio_test": "/api/negocio/test",
            "registro_negocio": "/api/auth/registro_negocio",
            "perfil_negocio": "/api/negocio/perfil_negocio"
        }
    })

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return jsonify({
            "status": "info",
            "mensaje": "Usa POST con JSON para autenticarte",
            "ejemplo": {
                "usuario": "tu_correo@ejemplo.com",
                "contrasena": "tu_contraseña"
            }
        }), 200
    return login_usuario()

@auth_bp.route("/registro_negocio", methods=["GET", "POST"])
def registro_negocio():
    if request.method == "GET":
        return jsonify({
            "status": "info",
            "mensaje": "Usa POST con JSON para registrar un negocio",
            "ejemplo": {
                "nombre": "Panadería La Bendición",
                "correo": "panaderia@ejemplo.com",
                "telefono": "5551234567",
                "direccion": "Av. Principal 123",
                "descripcion": "Pan recién horneado todos los días",
                "disponibilidad": "5:00 AM - 9:00 PM",
                "tipo_entrega": "domicilio",
                "contrasena": "panconchocolate123"
            }
        }), 200
    return registro_negocio()

@auth_bp.route("/protegido", methods=["GET"])
@jwt_required()
def protegido():
    usuario = get_jwt_identity()
    return jsonify({
        "status": "success",
        "mensaje": f"Hola {usuario}, accediste a una ruta protegida",
        "usuario": usuario
    }), 200

# Rutas de negocio
@negocio_bp.route("/test", methods=["GET"])
def test_negocio():
    return jsonify({
        "status": "success",
        "mensaje": "Ruta de negocio funcionando correctamente"
    }), 200
