from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
import pymysql
from ..utils.jwt_utils import token_required
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

negocio_bp = Blueprint('negocio', __name__)

def get_db_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@negocio_bp.route('/perfil_negocio', methods=['GET'])
@token_required
def obtener_perfil():
    try:
        # Obtener el ID del negocio del token
        current_user = get_jwt_identity()
        negocio_id = current_user['user_id']
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Obtener datos del negocio
            sql = """
                SELECT id, nombre, correo, telefono, direccion, 
                       descripcion, disponibilidad, tipo_entrega
                FROM Negocio 
                WHERE id = %s
            """
            cursor.execute(sql, (negocio_id,))
            negocio = cursor.fetchone()
            
            if not negocio:
                return jsonify({
                    'error': 'Negocio no encontrado'
                }), 404
            
            return jsonify({
                'mensaje': 'Perfil obtenido exitosamente',
                'negocio': negocio
            }), 200
            
    except Exception as e:
        logger.error(f"Error al obtener perfil: {str(e)}")
        return jsonify({
            'error': 'Error al obtener el perfil',
            'mensaje': str(e)
        }), 500
    finally:
        connection.close()

@negocio_bp.route('/perfil_negocio', methods=['PUT'])
@token_required
def actualizar_perfil():
    try:
        current_user = get_jwt_identity()
        negocio_id = current_user['user_id']
        data = request.get_json()
        
        # Validar datos permitidos
        campos_permitidos = ['nombre', 'telefono', 'direccion', 'descripcion', 
                           'disponibilidad', 'tipo_entrega']
        datos_actualizar = {k: v for k, v in data.items() if k in campos_permitidos}
        
        if not datos_actualizar:
            return jsonify({
                'error': 'No hay datos válidos para actualizar'
            }), 400
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Construir query dinámica
            campos = ', '.join([f"{k} = %s" for k in datos_actualizar.keys()])
            valores = list(datos_actualizar.values())
            valores.append(negocio_id)
            
            sql = f"""
                UPDATE Negocio 
                SET {campos}
                WHERE id = %s
            """
            cursor.execute(sql, valores)
            connection.commit()
            
            return jsonify({
                'mensaje': 'Perfil actualizado exitosamente'
            }), 200
            
    except Exception as e:
        logger.error(f"Error al actualizar perfil: {str(e)}")
        return jsonify({
            'error': 'Error al actualizar el perfil',
            'mensaje': str(e)
        }), 500
    finally:
        connection.close() 