#WebServiceFlash/app/routes/dashboardCliente/negocioyProductos_cliente.py
from flask import Blueprint, jsonify
from mysql.connector import connect, Error
from config import Config
import base64  #  Para codificar imágenes en base64

negocioyProductos_dashboardClientes_bp = Blueprint('negocioyProductos_dashboardClientes_bp', __name__)

# Obtener conexión a la base de datos ----------------------------------------------------
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

# Obtener perfil público del negocio ----------------------------------------------------
@negocioyProductos_dashboardClientes_bp.route('/negocioyProductos/<int:negocio_id>', methods=['GET'])
def public_profile_negocio(negocio_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'mensaje': 'Error al conectar con la base de datos'}), 500
    try:
        cursor = connection.cursor()
        
        # Consulta el negocio (sin dictionary=True para procesar manualmente)
        cursor.execute("""
            SELECT id, nombre, categoria, telefono, correo, descripcion, direccion,
                   disponibilidad, tipo_entrega, profile_image
            FROM Negocio 
            WHERE id = %s
        """, (negocio_id,))
        
        row = cursor.fetchone()
        if not row:
            return jsonify({'status': 'error', 'mensaje': 'Negocio no encontrado'}), 404

        # ----------Convertir a diccionario manualmente
        keys = [desc[0] for desc in cursor.description]
        negocio = dict(zip(keys, row))

        # ----------Convertir imagen de bytes a base64 si existe
        if negocio['profile_image']:
            negocio['profile_image'] = base64.b64encode(negocio['profile_image']).decode('utf-8')
        else:
            negocio['profile_image'] = None

        return jsonify({'status': 'success', 'negocio': negocio})

    except Error as e:
        print(f"Error al consultar negocio: {e}")
        return jsonify({'status': 'error', 'mensaje': 'Error al obtener los datos'}), 500
    finally:
        cursor.close()
        connection.close()




# Obtener productos del negocio ----------------------------------------------------
@negocioyProductos_dashboardClientes_bp.route('/negocioyProductos/<int:negocio_id>/productos', methods=['GET'])
def productos_por_negocio(negocio_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'mensaje': 'Error al conectar con la base de datos'}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nombre, descripcion, precio, categoria, stock, fecha_creacion
            FROM Productos
            WHERE negocio_id = %s
        """, (negocio_id,))
        productos = cursor.fetchall()
        
        # Agregar URL de imagen a cada producto
        for producto in productos:
            producto['imagen_url'] = f"/api/productos/{producto['id']}/imagen"
        
        return jsonify({'status': 'success', 'productos': productos})
    except Error as e:
        print(f"Error al obtener productos del negocio: {e}")
        return jsonify({'status': 'error', 'mensaje': 'No se pudieron obtener los productos'}), 500
    finally:
        cursor.close()
        connection.close()
# Obtener imagen de producto ----------------------------------------------------