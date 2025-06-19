# app/__init__.py
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from app.routes.autenticacion.auth_controller import jwt_blacklist

jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blacklist

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    CORS(app)
    jwt.init_app(app)

    # Ruta raíz (aqui se ponen los endpoints disponibles, primero el prefijo de API, luego el nombre del archivo y la función)
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
                "Perfil Negocio": "/api/perfilNegocio/perfilNegocio",
                "Perfil Cliente": "/api/perfilCliente/perfilCliente",
                "Perfil Repartidor": "/api/perfilRepartidor/perfilRepartidor",
                "Editar Perfil Repartidor": "/api/perfilRepartidor/editarPerfil",
                "Dashboard (mostrar negocios a los usuarios)": "/api/dashboard_mostrar_negocios/dashboard_negocios",
                "Mostrar perfil de negocio a clientes y productos (Dashboard)": "/api/negocioyProductos"
            }
        })

    # Registrar blueprints (es decir los archivos de python)
    from app.routes.autenticacion.auth_controller import auth_bp
    from app.routes.perfiles.perfil_negocio_controller import perfil_negocio_bp
    from app.routes.perfiles.perfil_cliente_controller import perfil_cliente_bp
    from app.routes.perfiles.perfil_repartidor_controller import perfil_repartidor_bp
    from app.routes.dashboardCliente.dashboard_mostrar_negocios_controller import dashboard_mostrar_negocios_bp
    from app.routes.dashboardCliente.negocioyProductos_cliente import negocioyProductos_dashboardClientes_bp
    from app.routes.dashboardNegocio.productos_controller import productos_bp
    from app.routes.dashboardRepartidor.pedidos_repartidor_controller import pedidos_repartidor_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(perfil_negocio_bp, url_prefix='/api/perfilNegocio')
    app.register_blueprint(perfil_cliente_bp, url_prefix='/api/perfilCliente')
    app.register_blueprint(perfil_repartidor_bp, url_prefix='/api/perfilRepartidor')
    app.register_blueprint(dashboard_mostrar_negocios_bp, url_prefix='/api/dashboard_mostrar_negocios')
    app.register_blueprint(negocioyProductos_dashboardClientes_bp, url_prefix='/api/negocioyProductos')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')
    app.register_blueprint(pedidos_repartidor_bp, url_prefix='/api/pedidos')


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
