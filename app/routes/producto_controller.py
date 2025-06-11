from flask import Blueprint, jsonify
from mysql.connector import connect, Error
from config import Config

producto_publico_bp = Blueprint('producto_publico_bp', __name__)

def get_db_connection():
    try:
        connection = connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

@producto_publico_bp.route('/public_profile/<int:negocio_id>', methods=['GET'])
def public_profile_negocio(negocio_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'mensaje': 'Error al conectar con la base de datos'}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        # Obtener datos del negocio
        cursor.execute("""
            SELECT id, nombre, categoria, telefono, correo, descripcion, direccion, disponibilidad, tipo_entrega
            FROM Negocio WHERE id = %s
        """, (negocio_id,))
        negocio = cursor.fetchone()
        if not negocio:
            return jsonify({'status': 'error', 'mensaje': 'Negocio no encontrado'}), 404
        return jsonify({'status': 'success', 'negocio': negocio})
    except Error as e:
        print(f"Error al consultar negocio: {e}")
        return jsonify({'status': 'error', 'mensaje': 'Error al obtener los datos'}), 500
    finally:
        cursor.close()
        connection.close()
