from flask import request, jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_identity
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

def registro():
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
            cursor.execute("SELECT id FROM Negocio WHERE correo = %s", (data['correo'],))
            if cursor.fetchone():
                return jsonify({'error': 'El correo ya está registrado'}), 409
            
            sql = """
                INSERT INTO Negocio 
                (nombre, correo, contrasena, telefono, direccion, descripcion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['nombre'],
                data['correo'],
                hashed_pw,
                data.get('telefono', ''),
                data.get('direccion', ''),
                data.get('descripcion', '')
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

def login():
    conn = None
    try:
        data = request.get_json()
        
        if 'correo' not in data or 'contrasena' not in data:
            return jsonify({'error': 'Credenciales incompletas'}), 400

        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Negocio WHERE correo = %s", (data['correo'],))
            negocio = cursor.fetchone()
            
            if not negocio or not check_password_hash(negocio['contrasena'], data['contrasena']):
                return jsonify({'error': 'Credenciales inválidas'}), 401
            
            identity = {
                'id': negocio['id'],
                'correo': negocio['correo']
            }
            
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)
            
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'negocio': {
                    'id': negocio['id'],
                    'nombre': negocio['nombre'],
                    'correo': negocio['correo']
                }
            }), 200

    except pymysql.MySQLError as e:
        logger.error(f"Error de MySQL en login: {str(e)}")
        return jsonify({'error': 'Error en la base de datos'}), 500
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error en el servidor'}), 500
    finally:
        if conn:
            conn.close()

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.add_url_rule('/registro', view_func=registro, methods=['POST'])
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])