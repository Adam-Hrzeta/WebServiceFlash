from app.routes.administracion import usuarios_admin_controller, dashboard_admin_controller
# app/__init__.py
# Archivo principal de configuración y arranque de la aplicación Flask
from flask import Flask, jsonify, redirect  # Importación de Flask y utilidades
from flask_cors import CORS  # Permite peticiones desde otros dominios
from flask_jwt_extended import JWTManager  # Manejo de autenticación JWT
from config import Config  # Configuración de la app (variables de entorno, DB, etc)
from app.routes.autenticacion.auth_controller import jwt_blacklist  # Lista negra de tokens JWT

jwt = JWTManager()  # Instancia global de JWT

@jwt.token_in_blocklist_loader  # Verifica si el token está en la blacklist
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blacklist

def create_app():
    # Función principal para crear y configurar la app Flask
    app = Flask(__name__)  # Instancia de la aplicación Flask
    app.config.from_object(Config)  # Carga la configuración

    # Inicializar extensiones
    CORS(app)  # Habilita CORS
    jwt.init_app(app)  # Inicializa JWT en la app

    # Ruta raíz: muestra el estado y todos los endpoints disponibles
    @app.route('/')  # Endpoint principal para documentación rápida
    def root():
        return jsonify({
            "status": "Web Service Funcionando Correctamente",
            "mensaje": "Web service de la aplicación FlashEnd",
            "documentacion": "Para ver la documentación completa, visita /api/auth/",
            "endpoints": {
                "Login (inicio de sesión)": "/api/auth/login",
                "Registro Negocio": "/api/auth/registro_Negocio",
                "Registro Cliente": "/api/auth/registro_Cliente",
                "Registro Repartidor": "/api/auth/registro_Repartidor",
                "Verificar correo": "/api/auth/verificar_correo",
                "Recuperar contraseña": "/api/auth/recuperar_contrasena",
                "Renovar token": "/api/auth/refresh",
                "Perfil Negocio (obtener)": "/api/perfilNegocio/perfilNegocio",
                "Perfil Negocio (test)": "/api/perfilNegocio/test",
                "Perfil Negocio (subir imagen)": "/api/perfilNegocio/upload_profile_image",
                "Perfil Negocio (obtener imagen)": "/api/perfilNegocio/profile_image?id=<negocio_id>",
                "Perfil Negocio (editar perfil)": "/api/perfilNegocio/editarPerfil",
                "Productos (listar)": "/api/productos/",
                "Productos (crear)": "/api/productos/",
                "Productos (obtener imagen)": "/api/productos/<producto_id>/imagen",
                "Productos (actualizar)": "/api/productos/<producto_id>",
                "Productos (eliminar)": "/api/productos/<producto_id>",
                "Pedidos Negocio (pendientes)": "/api/pedidos_negocio/pedidos_pendientes",
                "Pedidos Negocio (aceptar)": "/api/pedidos_negocio/aceptar_pedido/<pedido_id>",
                "Pedidos Negocio (enviar)": "/api/pedidos_negocio/enviar_pedido/<pedido_id>",
                "Pedidos Negocio (entregado)": "/api/pedidos_negocio/marcar_entregado/<pedido_id>",
                "Perfil Cliente (obtener)": "/api/perfilCliente/perfilCliente",
                "Perfil Cliente (subir imagen)": "/api/perfilCliente/upload_profile_image",
                "Perfil Cliente (obtener imagen)": "/api/perfilCliente/profile_image?id=<cliente_id>",
                "Perfil Cliente (editar perfil)": "/api/perfilCliente/editarPerfil",
                "Dashboard Cliente (test)": "/api/dashboard_mostrar_negocios/test",
                "Dashboard Cliente (listar negocios)": "/api/dashboard_mostrar_negocios/dashboard_negocios",
                "Dashboard Cliente (obtener negocio)": "/api/dashboard_mostrar_negocios/negocio/<id>",
                "Perfil público negocio": "/api/negocioyProductos/negocioyProductos/<negocio_id>",
                "Productos por negocio": "/api/negocioyProductos/negocioyProductos/<negocio_id>/productos",
                "Realizar pedido": "/api/pedidos_cliente/realizar_pedido",
                "Historial de pedidos": "/api/pedidos_cliente/historial",
                "Confirmar entrega de pedido": "/api/pedidos_cliente/confirmar_entrega/<pedido_id>",
                "Perfil Repartidor (obtener)": "/api/perfilRepartidor/perfilRepartidor",
                "Perfil Repartidor (test)": "/api/perfilRepartidor/test",
                "Perfil Repartidor (subir imagen)": "/api/perfilRepartidor/upload_profile_image",
                "Perfil Repartidor (obtener imagen)": "/api/perfilRepartidor/profile_image?id=<repartidor_id>",
                "Perfil Repartidor (editar perfil)": "/api/perfilRepartidor/editarPerfil",
                "Pedidos Repartidor (asignados)": "/api/pedidos/pedidos_asignados",
                "Negocios pendientes": "/api/dashboard_admin/negocios_pendientes",
                "Repartidores pendientes": "/api/dashboard_admin/repartidores_pendientes",
                "Aprobar negocio": "/api/dashboard_admin/aprobar_negocio/<negocio_id>",
                "Rechazar negocio": "/api/dashboard_admin/rechazar_negocio/<negocio_id>",
                "Aprobar repartidor": "/api/dashboard_admin/aprobar_repartidor/<repartidor_id>",
                "Rechazar repartidor": "/api/dashboard_admin/rechazar_repartidor/<repartidor_id>"
            }
        })

    # Importar todos los blueprints y controladores
    # Cada blueprint agrupa rutas relacionadas bajo un prefijo
    from app.routes.autenticacion.auth_controller import auth_bp  # Autenticación y registro
    from app.routes.perfil_Negocio.perfil_negocio_controller import perfil_negocio_bp  # Perfil de negocios
    from app.routes.perfil_Cliente.perfil_cliente_controller import perfil_cliente_bp  # Perfil de clientes
    from app.routes.perfil_Repartidor.perfil_repartidor_controller import perfil_repartidor_bp  # Perfil de repartidores
    from app.routes.perfil_Cliente.dashboard_mostrar_negocios_controller import dashboard_mostrar_negocios_bp  # Dashboard de negocios para clientes
    from app.routes.perfil_Cliente.negocioyProductos_cliente import negocioyProductos_dashboardClientes_bp  # Perfil público de negocios y productos
    from app.routes.perfil_Negocio.gestion_pedidos_controller import pedidos_negocio_bp  # Gestión de pedidos para negocios
    from app.routes.perfil_Repartidor.pedidos_repartidor_controller import pedidos_repartidor_bp  # Pedidos asignados a repartidores
    from app.routes.perfil_Cliente.pedidos_cliente import pedidos_cliente_bp  # Pedidos realizados por clientes
    from app.routes.perfil_Negocio.productos_controller import productos_bp  # Gestión de productos
    from app.routes.administracion.blueprints import dashboard_admin_bp  # Blueprint para administración (incluye usuarios admin)

    # Registrar blueprints en la app Flask
    # Cada blueprint se asocia a un prefijo de URL y agrupa rutas relacionadas
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # Rutas de autenticación y registro
    app.register_blueprint(perfil_negocio_bp, url_prefix='/api/negocio')  # Rutas de perfil de negocio
    app.register_blueprint(perfil_cliente_bp, url_prefix='/api/perfilCliente')  # Rutas de perfil de cliente
    app.register_blueprint(perfil_repartidor_bp, url_prefix='/api/perfilRepartidor')  # Rutas de perfil de repartidor
    app.register_blueprint(dashboard_mostrar_negocios_bp, url_prefix='/api/dashboard_mostrar_negocios')  # Dashboard de negocios para clientes
    app.register_blueprint(negocioyProductos_dashboardClientes_bp, url_prefix='/api/negocioyProductos')  # Perfil público de negocios y productos
    app.register_blueprint(pedidos_repartidor_bp, url_prefix='/api/pedidos')  # Pedidos asignados a repartidores
    app.register_blueprint(dashboard_admin_bp, url_prefix='/api/dashboard_admin')  # Dashboard y usuarios admin
    app.register_blueprint(pedidos_cliente_bp, url_prefix='/api/pedidos_cliente')  # Pedidos realizados por clientes
    app.register_blueprint(pedidos_negocio_bp, url_prefix='/api/pedidos_negocio')  # Pedidos gestionados por negocios
    app.register_blueprint(productos_bp, url_prefix='/api/productos')  # Gestión de productos

    # Manejo de errores globales
    @app.errorhandler(404)  # Error: ruta no encontrada
    def not_found(error):
        return jsonify({
            "status": "error",
            "error": "Ruta no encontrada",
            "mensaje": "La ruta solicitada no existe. Visita / para ver los endpoints disponibles"
        }), 404

    @app.errorhandler(405)  # Error: método HTTP no permitido
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "error": "Método no permitido",
            "mensaje": "El método HTTP utilizado no está permitido para esta ruta"
        }), 405

    @app.errorhandler(500)  # Error interno del servidor
    def internal_error(error):
        return jsonify({
            "status": "error",
            "error": "Error interno del servidor",
            "mensaje": "Ha ocurrido un error inesperado"
        }), 500

    return app  # Devuelve la instancia configurada de la app Flask
