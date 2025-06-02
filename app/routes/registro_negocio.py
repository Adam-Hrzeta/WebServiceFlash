from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
import pymysql
from ..utils.jwt_utils import hash_password, verify_password, create_token_payload
from ..models.negocio import NegocioCreate, NegocioLogin
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('registro_negocio', __name__)

def get_db_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@auth_bp.route('/registro_negocio', methods=['POST'])
def registro_negocio():
    try:
        data = request.get_json()
        negocio = NegocioCreate(**data)
        
        # Hash de la contraseña
        hashed_password = hash_password(negocio.contrasena)
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Verificar si el correo ya existe
            sql = "SELECT id FROM Negocio WHERE correo = %s"
            cursor.execute(sql, (negocio.correo,))
            if cursor.fetchone():
                return jsonify({
                    'error': 'El correo ya está registrado'
                }), 400
            
            # Insertar nuevo negocio
            sql = """
                INSERT INTO Negocio (nombre, correo, telefono, direccion, 
                                   descripcion, disponibilidad, tipo_entrega, contrasena)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                negocio.nombre, negocio.correo, negocio.telefono,
                negocio.direccion, negocio.descripcion, negocio.disponibilidad,
                negocio.tipo_entrega, hashed_password
            ))
            connection.commit()
            
            return jsonify({
                'mensaje': 'Negocio registrado exitosamente'
            }), 201
            
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({
            'error': 'Error al registrar el negocio',
            'mensaje': str(e)
        }), 500
    finally:
        connection.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        login_data = NegocioLogin(**data)
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Buscar usuario por correo
            sql = "SELECT * FROM Negocio WHERE correo = %s"
            cursor.execute(sql, (login_data.correo,))
            negocio = cursor.fetchone()
            
            if not negocio:
                return jsonify({
                    'error': 'Credenciales inválidas'
                }), 401
            
            # Verificar contraseña
            if not verify_password(negocio['contrasena'], login_data.contrasena):
                return jsonify({
                    'error': 'Credenciales inválidas'
                }), 401
            
            # Crear tokens
            token_payload = create_token_payload(
                negocio['id'],
                negocio['correo']
            )
            
            access_token = create_access_token(identity=token_payload)
            refresh_token = create_refresh_token(identity=token_payload)
            
            return jsonify({
                'mensaje': 'Login exitoso',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'negocio': {
                    'id': negocio['id'],
                    'nombre': negocio['nombre'],
                    'correo': negocio['correo']
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({
            'error': 'Error en el proceso de login',
            'mensaje': str(e)
        }), 500
    finally:
        connection.close() 