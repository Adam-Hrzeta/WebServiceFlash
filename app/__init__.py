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
                # --- AUTENTICACIÓN ---
                "Login (inicio de sesión)": "/api/auth/login",
                "Registro Negocio": "/api/auth/registro_Negocio",
                "Registro Cliente": "/api/auth/registro_Cliente",
                "Registro Repartidor": "/api/auth/registro_Repartidor",
                "Verificar correo": "/api/auth/verificar_correo",
                "Recuperar contraseña": "/api/auth/recuperar_contrasena",
                "Renovar token": "/api/auth/refresh",

                # --- PERFIL NEGOCIO ---
                "Perfil Negocio (obtener)": "/api/perfilNegocio/perfilNegocio",
                "Perfil Negocio (test)": "/api/perfilNegocio/test",
                "Perfil Negocio (subir imagen)": "/api/perfilNegocio/upload_profile_image",
                "Perfil Negocio (obtener imagen)": "/api/perfilNegocio/profile_image?id=<negocio_id>",
                "Perfil Negocio (editar perfil)": "/api/perfilNegocio/editarPerfil",

                # --- PRODUCTOS (Negocio) ---
                "Productos (listar)": "/api/productos/",
                "Productos (crear)": "/api/productos/",
                "Productos (obtener imagen)": "/api/productos/<producto_id>/imagen",
                "Productos (actualizar)": "/api/productos/<producto_id>",
                "Productos (eliminar)": "/api/productos/<producto_id>",

                # --- GESTIÓN DE PEDIDOS (Negocio) ---
                "Pedidos Negocio (pendientes)": "/api/pedidos_negocio/pedidos_pendientes",
                "Pedidos Negocio (aceptar)": "/api/pedidos_negocio/aceptar_pedido/<pedido_id>",
                "Pedidos Negocio (enviar)": "/api/pedidos_negocio/enviar_pedido/<pedido_id>",
                "Pedidos Negocio (entregado)": "/api/pedidos_negocio/marcar_entregado/<pedido_id>",

                # --- PERFIL CLIENTE ---
                "Perfil Cliente (obtener)": "/api/perfilCliente/perfilCliente",
                "Perfil Cliente (subir imagen)": "/api/perfilCliente/upload_profile_image",
                "Perfil Cliente (obtener imagen)": "/api/perfilCliente/profile_image?id=<cliente_id>",
                "Perfil Cliente (editar perfil)": "/api/perfilCliente/editarPerfil",

                # --- DASHBOARD CLIENTE ---
                "Dashboard Cliente (test)": "/api/dashboard_mostrar_negocios/test",
                "Dashboard Cliente (listar negocios)": "/api/dashboard_mostrar_negocios/dashboard_negocios",
                "Dashboard Cliente (obtener negocio)": "/api/dashboard_mostrar_negocios/negocio/<id>",

                # --- Negocio público y productos para clientes ---
                "Perfil público negocio": "/api/negocioyProductos/negocioyProductos/<negocio_id>",
                "Productos por negocio": "/api/negocioyProductos/negocioyProductos/<negocio_id>/productos",

                # --- PEDIDOS CLIENTE ---
                "Realizar pedido": "/api/pedidos_cliente/realizar_pedido",
                "Historial de pedidos": "/api/pedidos_cliente/historial",
                "Confirmar entrega de pedido": "/api/pedidos_cliente/confirmar_entrega/<pedido_id>",

                # --- PERFIL REPARTIDOR ---
                "Perfil Repartidor (obtener)": "/api/perfilRepartidor/perfilRepartidor",
                "Perfil Repartidor (test)": "/api/perfilRepartidor/test",
                "Perfil Repartidor (subir imagen)": "/api/perfilRepartidor/upload_profile_image",
                "Perfil Repartidor (obtener imagen)": "/api/perfilRepartidor/profile_image?id=<repartidor_id>",
                "Perfil Repartidor (editar perfil)": "/api/perfilRepartidor/editarPerfil",

                # --- PEDIDOS REPARTIDOR ---
                "Pedidos Repartidor (asignados)": "/api/pedidos/pedidos_asignados",

                # --- DASHBOARD ADMINISTRADOR ---
                "Negocios pendientes": "/api/dashboard_admin/negocios_pendientes",
                "Repartidores pendientes": "/api/dashboard_admin/repartidores_pendientes",
                "Aprobar negocio": "/api/dashboard_admin/aprobar_negocio/<negocio_id>",
                "Rechazar negocio": "/api/dashboard_admin/rechazar_negocio/<negocio_id>",
                "Aprobar repartidor": "/api/dashboard_admin/aprobar_repartidor/<repartidor_id>",
                "Rechazar repartidor": "/api/dashboard_admin/rechazar_repartidor/<repartidor_id>"
            }
        })

    # Registrar blueprints (es decir los archivos de python)
    from app.routes.autenticacion.auth_controller import auth_bp
    from app.routes.perfil_Negocio.perfil_negocio_controller import perfil_negocio_bp
    from app.routes.perfil_Cliente.perfil_cliente_controller import perfil_cliente_bp
    from app.routes.perfil_Repartidor.perfil_repartidor_controller import perfil_repartidor_bp
    from app.routes.perfil_Cliente.dashboard_mostrar_negocios_controller import dashboard_mostrar_negocios_bp
    from app.routes.perfil_Cliente.negocioyProductos_cliente import negocioyProductos_dashboardClientes_bp
    from app.routes.perfil_Negocio.gestion_pedidos_controller import pedidos_negocio_bp
    from app.routes.perfil_Repartidor.pedidos_repartidor_controller import pedidos_repartidor_bp
    from app.routes.administracion.dashboard_admin_controller import dashboard_admin_bp
    from app.routes.perfil_Cliente.pedidos_cliente import pedidos_cliente_bp
    from app.routes.perfil_Negocio.productos_controller import productos_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(perfil_negocio_bp, url_prefix='/api/negocio')
    app.register_blueprint(perfil_cliente_bp, url_prefix='/api/perfilCliente')
    app.register_blueprint(perfil_repartidor_bp, url_prefix='/api/perfilRepartidor')
    app.register_blueprint(dashboard_mostrar_negocios_bp, url_prefix='/api/dashboard_mostrar_negocios')
    app.register_blueprint(negocioyProductos_dashboardClientes_bp, url_prefix='/api/negocioyProductos')
    app.register_blueprint(pedidos_repartidor_bp, url_prefix='/api/pedidos')
    app.register_blueprint(dashboard_admin_bp, url_prefix='/api/dashboard_admin')
    app.register_blueprint(pedidos_cliente_bp, url_prefix='/api/pedidos_cliente')
    app.register_blueprint(pedidos_negocio_bp, url_prefix='/api/pedidos_negocio')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')


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
