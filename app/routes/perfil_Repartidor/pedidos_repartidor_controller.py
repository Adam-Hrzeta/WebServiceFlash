from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config
import base64

pedidos_repartidor_bp = Blueprint('pedidos_repartidor_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@pedidos_repartidor_bp.route('/pedidos_asignados', methods=['GET'])
@jwt_required()
def obtener_pedidos_asignados():
    identity = get_jwt_identity()
    claims = get_jwt()

    if not claims or claims.get('tipo_usuario') != 'repartidor':
        return jsonify({'error': 'No autorizado'}), 403

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, c.nombre AS cliente_nombre, c.telefono AS cliente_telefono,
                       n.nombre AS negocio_nombre, n.telefono AS negocio_telefono, n.categoria
                FROM Pedidos p
                JOIN Cliente c ON p.cliente_id = c.id
                JOIN Negocio n ON p.negocio_id = n.id
                WHERE p.repartidor_id = %s
            """, (identity,))
            pedidos = cursor.fetchall()
            # Para cada pedido, obtener los productos
            for pedido in pedidos:
                cursor.execute("""
                    SELECT dp.*, pr.nombre, pr.descripcion, pr.precio, pr.imagen
                    FROM detalle_pedido dp
                    JOIN Productos pr ON dp.producto_id = pr.id
                    WHERE dp.pedido_id = %s
                """, (pedido['id'],))
                productos = cursor.fetchall()
                # Convertir imagen a string si es bytes
                for prod in productos:
                    if isinstance(prod.get('imagen'), bytes):
                        prod['imagen'] = base64.b64encode(prod['imagen']).decode('utf-8')
                pedido['productos'] = productos
            return jsonify({'pedidos': pedidos})
    finally:
        conn.close()

@pedidos_repartidor_bp.route('/aceptar_pedido/<int:pedido_id>', methods=['POST'])
@jwt_required()
def aceptar_pedido_repartidor(pedido_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'repartidor':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Pedidos SET estatus = 'en_camino' WHERE id = %s AND repartidor_id = %s
            """, (pedido_id, identity))
            conn.commit()
        return jsonify({'mensaje': 'Pedido aceptado por repartidor'})
    finally:
        conn.close()

@pedidos_repartidor_bp.route('/entregar_pedido/<int:pedido_id>', methods=['POST'])
@jwt_required()
def entregar_pedido_repartidor(pedido_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'repartidor':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Pedidos SET estatus = 'entregado' WHERE id = %s AND repartidor_id = %s
            """, (pedido_id, identity))
            conn.commit()
        return jsonify({'mensaje': 'Pedido entregado'})
    finally:
        conn.close()
