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
            "status": "Web Service Funcionando Correctamente",
            "mensaje": "Web service de la aplicación FlashEnd",
            "documentacion": "Para ver la documentación completa, visita /api/auth/",
            "endpoints": {
                "Inicio de sesión": "/api/auth/login",
                "Registro Negocio": "/api/auth/registro_Negocio",
                "Registro Cliente": "/api/auth/registro_Cliente",
                "Registro Repartidor": "/api/auth/registro_Repartidor",
                "Perfil Negocio": "/api/perfilNegocio/perfil_negocio",
                "Perfil Cliente": "/api/perfilCliente/perfil_cliente",
                "Perfil Repartidor": "/api/perfilRepartidor/perfil_repartidor",
                "Dashboard (mostrar negocios a los usuarios)": "/api/dashboard/dashboard_negocios",
            }
        })

    # Registrar blueprints
    from app.routes.auth_controller import auth_bp
    from app.routes.perfil_negocio_controller import perfil_negocio_bp
    from app.routes.perfil_cliente_controller import perfil_cliente_bp
    from app.routes.perfil_repartidor_controller import perfil_repartidor_bp
    from app.routes.dashboard_mostrar_negocios_controller import dashboard_mostrar_negocios_bp
    #implementar el blue print para el que el cliente pueda ver un negocio individual y poder hacer pedidos
    from app.routes.dashboard_mostrar_negocios_individual_controller import dashboard_mostrar_negocios_individual_bp
    #implementar el blue print para que el repartidor pueda ver los pedidos que tiene asignados
    from app.routes.dashboard_mostrar_pedidos_asignados_repartidor_controller import dashboard_mostrar_pedidos_repartidor_bp  


    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(perfil_negocio_bp, url_prefix='/api/perfilNegocio')
    app.register_blueprint(perfil_cliente_bp, url_prefix='/api/perfilCliente')
    app.register_blueprint(perfil_repartidor_bp, url_prefix='/api/perfilRepartidor')
    app.register_blueprint(dashboard_mostrar_negocios_bp, url_prefix='/api/dashboard_mostrar_negocios')


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
