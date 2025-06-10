from flask import Blueprint, jsonify, request
from mysql.connector import connect, Error
from config import Config

dashboard_mostrar_negocios_bp = Blueprint('dashboard_mostrar_negocios_bp', __name__)

dashboard_mostrar_negocios_bp.route('/dashboard_mostrar_Negocios', methods=['GET'])

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

@dashboard_mostrar_negocios_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de negocio funcionando'
    })

@dashboard_mostrar_negocios_bp.route('/dashboard_negocios', methods=['GET'])
def obtener_negocios():
    connection = get_db_connection()
    if not connection:
        return jsonify({
            'status': 'error',
            'mensaje': 'Error al conectar con la base de datos'
        }), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT id, nombre, correo, telefono, direccion, descripcion, 
               disponibilidad, tipo_entrega
        FROM Negocio
        """
        cursor.execute(query)
        negocios = cursor.fetchall()
        
        return jsonify({
            'status': 'success',
            'negocios': negocios
        })
    except Error as e:
        print(f"Error al consultar negocios: {e}")
        return jsonify({
            'status': 'error',
            'mensaje': 'Error al obtener los negocios'
        }), 500
    finally:
        cursor.close()
        connection.close()

@dashboard_mostrar_negocios_bp.route('/negocio/<int:id>', methods=['GET'])
def obtener_negocio(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({
            'status': 'error',
            'mensaje': 'Error al conectar con la base de datos'
        }), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT id, nombre, correo, telefono, direccion, descripcion, 
               disponibilidad, tipo_entrega
        FROM Negocio
        WHERE id = %s
        """
        cursor.execute(query, (id,))
        negocio = cursor.fetchone()
        
        if not negocio:
            return jsonify({
                'status': 'error',
                'mensaje': 'Negocio no encontrado'
            }), 404
        
        return jsonify({
            'status': 'success',
            'negocio': negocio
        })
    except Error as e:
        print(f"Error al consultar negocio: {e}")
        return jsonify({
            'status': 'error',
            'mensaje': 'Error al obtener el negocio'
        }), 500
    finally:
        cursor.close()
        connection.close()

@dashboard_mostrar_negocios_bp.route('/negocio', methods=['POST'])
def crear_negocio():
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'mensaje': 'No se proporcionaron datos'
        }), 400
    
    required_fields = ['nombre', 'correo', 'telefono', 'direccion', 'tipo_entrega', 'contrasena']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'mensaje': f'Falta el campo requerido: {field}'
            }), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({
            'status': 'error',
            'mensaje': 'Error al conectar con la base de datos'
        }), 500
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO Negocio (nombre, correo, telefono, direccion, descripcion, 
                            disponibilidad, tipo_entrega, contrasena, fecha_creacion, fecha_actualizacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        cursor.execute(query, (
            data['nombre'],
            data['correo'],
            data['telefono'],
            data['direccion'],
            data.get('descripcion'),
            data.get('disponibilidad', True),
            data['tipo_entrega'],
            data['contrasena']
        ))
        connection.commit()
        
        negocio_id = cursor.lastrowid
        
        return jsonify({
            'status': 'success',
            'mensaje': 'Negocio creado exitosamente',
            'negocio_id': negocio_id
        }), 201
    except Error as e:
        connection.rollback()
        print(f"Error al crear negocio: {e}")
        return jsonify({
            'status': 'error',
            'mensaje': 'Error al crear el negocio'
        }), 500
    finally:
        cursor.close()
        connection.close()
