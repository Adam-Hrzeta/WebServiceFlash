# app/__init__.py
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    CORS(app)
    jwt.init_app(app)

    # Ruta raíz
    @app.route('/')
    def root():
        return jsonify({
            "status": "success",
            "mensaje": "Bienvenido a la API",
            "documentacion": "Para ver la documentación completa, visita /api/auth/",
            "endpoints": {
                "documentacion": "/api/auth/",
                "login": "/api/auth/login",
                "protegido": "/api/auth/protegido",
                "negocio_test": "/api/negocio/test"
            }
        })

    # Registrar blueprints
    from .routes import auth_bp, negocio_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(negocio_bp, url_prefix='/api/negocio')

    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "error": "Ruta no encontrada",
            "mensaje": "La ruta solicitada no existe. Visita / para ver los endpoints disponibles"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "error": "Método no permitido",
            "mensaje": "El método HTTP utilizado no está permitido para esta ruta"
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "status": "error",
            "error": "Error interno del servidor",
            "mensaje": "Ha ocurrido un error inesperado"
        }), 500

    return app
