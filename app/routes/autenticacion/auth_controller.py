from flask import request, jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
import pymysql
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import re

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Definir blueprint al inicio para evitar NameError
auth_bp = Blueprint('auth_bp', __name__)

# REGISTRO DE NEGOCIO
def registroNegocio():
    conn = None
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'correo', 'contrasena', 'categoria']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos obligatorios: nombre, correo, contrasena, categoria'}), 400

        if not is_valid_email(data['correo']):
            return jsonify({'error': 'Formato de correo inválido'}), 400

        if len(data['contrasena']) < 8:
            return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400

        hashed_pw = generate_password_hash(data['contrasena'])
        
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM Negocio WHERE correo = %s", (data['correo'],))
            if cursor.fetchone():
                return jsonify({'error': 'El correo ya está registrado'}), 409
            
            sql = """
                INSERT INTO Negocio 
                (nombre, correo, contrasena, telefono, direccion, descripcion, categoria, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pendiente')
            """
            cursor.execute(sql, (
                data['nombre'],
                data['correo'],
                hashed_pw,
                data.get('telefono', ''),
                data.get('direccion', ''),
                data.get('descripcion', ''),
                data['categoria']
            ))
            conn.commit()
            
            return jsonify({'mensaje': 'Registro exitoso'}), 201

    except pymysql.MySQLError as e:
        logger.error(f"Error de MySQL en registro: {str(e)}")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if conn:
            conn.close()

# REGISTRO DE CLIENTE
def registroCliente():
    conn = None
    try:
        data = request.get_json()

        required_fields = ['nombre', 'correo', 'contrasena']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos obligatorios: nombre, correo, contrasena'}), 400
        
        if not is_valid_email(data['correo']):
            return jsonify({'error': 'Formato de correo inválido'}), 400
        
        if len(data['contrasena']) < 8:
            return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400
        
        hashed_pw = generate_password_hash(data['contrasena'])

        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM Cliente WHERE correo = %s", (data['correo'],))
            if cursor.fetchone():
                return jsonify({'error': 'El correo ya está registrado'}), 409
            
            sql = """
                INSERT INTO Cliente 
                (nombre, correo, telefono, contrasena, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['nombre'],
                data['correo'],
                data.get('telefono', ''),
                hashed_pw,
                data.get('fecha_nacimiento', None)
            ))
            conn.commit()
            
            return jsonify({'mensaje': 'Registro exitoso'}), 201
    except pymysql.MySQLError as e:
        logger.error(f"Error de MySQL en registro: {str(e)}")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if conn:
            conn.close()

# REGISTRO DE REPARTIDOR
def registroRepartidor():
    import traceback
    conn = None
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'correo', 'contrasena']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos obligatorios: nombre, correo, contrasena'}), 400

        if not is_valid_email(data['correo']):
            return jsonify({'error': 'Formato de correo inválido'}), 400

        if len(data['contrasena']) < 8:
            return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400

        hashed_pw = generate_password_hash(data['contrasena'])
        
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM Repartidor WHERE correo = %s", (data['correo'],))
            if cursor.fetchone():
                return jsonify({'error': 'El correo ya está registrado'}), 409
            
            sql = """
                INSERT INTO Repartidor 
                (nombre, correo, telefono, fecha_nacimiento, contrasena, disponibilidad, tipo_servicio, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pendiente')
            """
            cursor.execute(sql, (
                data['nombre'],
                data['correo'],
                data.get('telefono', ''),
                data.get('fecha_nacimiento', ''),
                hashed_pw,
                data.get('disponibilidad', ''),
                data.get('tipo_servicio', 'Cuenta Propia' if 'empresa' not in data else 'Empresa')
            ))
            conn.commit()
            
            return jsonify({'mensaje': 'Registro exitoso'}), 201

    except pymysql.MySQLError as e:
        logger.error(f"Error de MySQL en registro: {str(e)}")
        return jsonify({'error': 'Error en la base de datos', 'detalle': str(e), 'traceback': traceback.format_exc()}), 500
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error en el servidor', 'detalle': str(e), 'traceback': traceback.format_exc()}), 500
    finally:
        if conn:
            conn.close()

# INICIO DE SESIÓN PARA TODOS LOS USUARIOS
def login():
    conn = None
    try:
        data = request.get_json()
        
        if 'correo' not in data or 'contrasena' not in data:
            return jsonify({'error': 'Credenciales incompletas'}), 400

        conn = get_db()
        with conn.cursor() as cursor:
            # Buscar primero en Negocio
            cursor.execute("SELECT * FROM Negocio WHERE correo = %s", (data['correo'],))
            negocio = cursor.fetchone()
            if negocio and check_password_hash(negocio['contrasena'], data['contrasena']):
                if negocio.get('estado') != 'aprobado':
                    return jsonify({'error': 'Tu cuenta aún no ha sido aprobada por el administrador.'}), 403
                identity = str(negocio['id'])
                additional_claims = {
                    'correo': negocio['correo'],
                    'tipo_usuario': 'negocio'
                }
                access_token = create_access_token(identity=identity, additional_claims=additional_claims)
                refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'negocio': {
                        'id': negocio['id'],
                        'nombre': negocio['nombre'],
                        'correo': negocio['correo']
                    },
                    'tipo_usuario': 'negocio' 
                }), 200
            # Si no es negocio, buscar en Cliente
            cursor.execute("SELECT * FROM Cliente WHERE correo = %s", (data['correo'],))
            cliente = cursor.fetchone()
            if cliente and check_password_hash(cliente['contrasena'], data['contrasena']):
                identity = str(cliente['id'])
                additional_claims = {
                    'correo': cliente['correo'],
                    'tipo_usuario': 'cliente'
                }
                access_token = create_access_token(identity=identity, additional_claims=additional_claims)
                refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'cliente': {
                        'id': cliente['id'],
                        'nombre': cliente['nombre'],
                        'correo': cliente['correo']
                    },
                    'tipo_usuario': 'cliente' 
                }), 200
            # Si no es cliente, buscar en Repartidor
            cursor.execute("SELECT * FROM Repartidor WHERE correo = %s", (data['correo'],))
            administrador = cursor.fetchone()
            if administrador and check_password_hash(administrador['contrasena'], data['contrasena']):
                identity = str(administrador['id'])
                additional_claims = {
                    'correo': administrador['correo'],
                    'tipo_usuario': 'repartidor'
                }
                access_token = create_access_token(identity=identity, additional_claims=additional_claims)
                refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'repartidor': {
                        'id': administrador['id'],
                        'nombre': administrador['nombre'],
                        'correo': administrador['correo']
                    },
                    'tipo_usuario': 'repartidor' 
                }), 200
            # Si no es repartidor, buscar en administrador
            cursor.execute("SELECT * FROM Administradores WHERE correo = %s", (data['correo'],))
            administrador = cursor.fetchone()
            if administrador and check_password_hash(administrador['contrasena'], data['contrasena']):
                identity = str(administrador['id'])
                additional_claims = {
                    'correo': administrador['correo'],
                    'tipo_usuario': 'administrador'
                }
                access_token = create_access_token(identity=identity, additional_claims=additional_claims)
                refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'administrador': {
                        'id': administrador['id'],
                        'nombre': administrador['nombre'],
                        'correo': administrador['correo']
                    },
                    'tipo_usuario': 'administrador' 
                }), 200
            # Si no se encontró en ninguna tabla
            return jsonify({'error': 'Credenciales inválidas'}), 401

    except pymysql.MySQLError as e:
        logger.error(f"Error de MySQL en login: {str(e)}")
        return jsonify({'error': 'Error en la base de datos', 'detalle': str(e)}), 500
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error en el servidor', 'detalle': str(e)}), 500
    finally:
        if conn:
            conn.close()

# Blacklist simple en memoria para tokens JWT
jwt_blacklist = set()

# Endpoint logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200

# Registrar endpoints
auth_bp.add_url_rule('/registro_Cliente', view_func=registroCliente, methods=['POST'])
auth_bp.add_url_rule('/registro_Negocio', view_func=registroNegocio, methods=['POST'])
auth_bp.add_url_rule('/registro_Repartidor', view_func=registroRepartidor, methods=['POST'])
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])