# app/__init__.py
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from app.routes.autenticacion.auth_controller import jwt_blacklist

jwt = JWTManager()

@jwt.token_in_blocklist_loader  # Corregido el nombre del decorador
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
                "Mostrar perfil de negocio a clientes y productos (Dashboard)": "/api/negocioyProductos",
                "Perfil Negocio (test)": "/api/perfilNegocio/test",
                "Perfil Negocio (subir imagen)": "/api/perfilNegocio/upload_profile_image",
                "Perfil Negocio (obtener imagen)": "/api/perfilNegocio/profile_image",
                "Perfil Negocio (editar perfil)": "/api/perfilNegocio/editarPerfil",
                "Perfil Cliente (subir imagen)": "/api/perfilCliente/upload_profile_image",
                "Perfil Cliente (obtener imagen)": "/api/perfilCliente/profile_image",
                "Perfil Cliente (editar perfil)": "/api/perfilCliente/editarPerfil",
                "Perfil Repartidor (test)": "/api/perfilRepartidor/test",
                "Perfil Repartidor (subir imagen)": "/api/perfilRepartidor/upload_profile_image",
                "Perfil Repartidor (obtener imagen)": "/api/perfilRepartidor/profile_image",
                "Perfil Repartidor (editar perfil)": "/api/perfilRepartidor/editarPerfil",
                "Productos (listar)": "/api/productos/",
                "Productos (crear)": "/api/productos/",
                "Productos (obtener imagen)": "/api/productos/<producto_id>/imagen",
                "Productos (actualizar)": "/api/productos/<producto_id>",
                "Productos (eliminar)": "/api/productos/<producto_id>",
                "Dashboard Cliente (test)": "/api/dashboard_mostrar_negocios/test",
                "Dashboard Cliente (listar negocios)": "/api/dashboard_mostrar_negocios/dashboard_negocios",
                "Dashboard Cliente (obtener negocio)": "/api/dashboard_mostrar_negocios/negocio/<id>",
                "Dashboard Cliente (crear negocio)": "/api/dashboard_mostrar_negocios/negocio",
                "Dashboard Cliente (perfil público negocio)": "/api/negocioyProductos/negocioyProductos/<negocio_id>",
                "Dashboard Cliente (productos por negocio)": "/api/negocioyProductos/negocioyProductos/<negocio_id>/productos",
                "Pedidos Repartidor (asignados)": "/api/pedidos/pedidos_asignados",
                "Dashboard Admin (negocios pendientes)": "/api/dashboard_admin/negocios_pendientes",
                "Dashboard Admin (repartidores pendientes)": "/api/dashboard_admin/repartidores_pendientes",
                "Dashboard Admin (aprobar negocio)": "/api/dashboard_admin/aprobar_negocio/<negocio_id>",
                "Dashboard Admin (rechazar negocio)": "/api/dashboard_admin/rechazar_negocio/<negocio_id>",
                "Dashboard Admin (aprobar repartidor)": "/api/dashboard_admin/aprobar_repartidor/<repartidor_id>",
                "Dashboard Admin (rechazar repartidor)": "/api/dashboard_admin/rechazar_repartidor/<repartidor_id>",
                "Pedidos Negocio (pendientes)": "/api/pedidos_negocio/pedidos_pendientes",
                "Pedidos Negocio (aceptar)": "/api/pedidos_negocio/aceptar_pedido/<pedido_id>",
                "Pedidos Negocio (enviar)": "/api/pedidos_negocio/enviar_pedido/<pedido_id>",
                "Pedidos Negocio (entregado)": "/api/pedidos_negocio/marcar_entregado/<pedido_id>"
            }
        })

    # Registrar blueprints (es decir los archivos de python)
    from app.routes.autenticacion.auth_controller import auth_bp
    from app.routes.perfil_Negocio.perfil_negocio_controller import perfil_negocio_bp
    from app.routes.perfiles.perfil_cliente_controller import perfil_cliente_bp
    from app.routes.perfiles.perfil_repartidor_controller import perfil_repartidor_bp
    from app.routes.dashboardCliente.dashboard_mostrar_negocios_controller import dashboard_mostrar_negocios_bp
    from app.routes.dashboardCliente.negocioyProductos_cliente import negocioyProductos_dashboardClientes_bp
    from app.routes.perfil_Negocio.gestion_pedidos_controller import pedidos_negocio_bp
    from app.routes.dashboardRepartidor.pedidos_repartidor_controller import pedidos_repartidor_bp
    from app.routes.dashboardAdmin.dashboard_admin_controller import dashboard_admin_bp
    from app.routes.dashboardCliente.pedidos_cliente import pedidos_cliente_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(perfil_negocio_bp, url_prefix='/api/perfilNegocio')
    app.register_blueprint(perfil_cliente_bp, url_prefix='/api/perfilCliente')
    app.register_blueprint(perfil_repartidor_bp, url_prefix='/api/perfilRepartidor')
    app.register_blueprint(dashboard_mostrar_negocios_bp, url_prefix='/api/dashboard_mostrar_negocios')
    app.register_blueprint(negocioyProductos_dashboardClientes_bp, url_prefix='/api/negocioyProductos')
    app.register_blueprint(pedidos_repartidor_bp, url_prefix='/api/pedidos')
    app.register_blueprint(dashboard_admin_bp, url_prefix='/api/dashboard_admin')
    app.register_blueprint(pedidos_cliente_bp, url_prefix='/api/pedidos_cliente')
    app.register_blueprint(pedidos_negocio_bp, url_prefix='/api/pedidos_negocio')


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
