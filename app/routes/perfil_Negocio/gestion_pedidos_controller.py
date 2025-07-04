from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config
import json
import base64

# Blueprint para gestión de pedidos del negocio
pedidos_negocio_bp = Blueprint('pedidos_negocio_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# 1. Listar pedidos pendientes y preparando para el negocio
@pedidos_negocio_bp.route('/pedidos_pendientes', methods=['GET'])
@jwt_required()
def listar_pedidos_pendientes():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, c.nombre AS cliente_nombre
                FROM Pedidos p
                JOIN Cliente c ON p.cliente_id = c.id
                WHERE p.negocio_id = %s AND (p.estatus = 'pendiente' OR p.estatus = 'preparando' OR p.estatus = 'enviado' OR p.estatus = 'en_camino' OR p.estatus = 'entregado')
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

# 2. Cambiar estatus a 'preparando' (aceptar pedido)
@pedidos_negocio_bp.route('/aceptar_pedido/<int:pedido_id>', methods=['POST'])
@jwt_required()
def aceptar_pedido(pedido_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Pedidos SET estatus = 'preparando' WHERE id = %s AND negocio_id = %s
            """, (pedido_id, identity))
            conn.commit()
        return jsonify({'mensaje': 'Pedido aceptado y en preparación'})
    finally:
        conn.close()

# 3. Cambiar estatus a 'enviado'
@pedidos_negocio_bp.route('/enviar_pedido/<int:pedido_id>', methods=['POST'])
@jwt_required()
def enviar_pedido_con_repartidor(pedido_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    data = request.get_json()
    repartidor_id = data.get('repartidor_id')
    if not repartidor_id:
        return jsonify({'error': 'Falta repartidor_id'}), 400
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Pedidos SET estatus = 'enviado', repartidor_id = %s WHERE id = %s AND negocio_id = %s",
                (repartidor_id, pedido_id, identity)
            )
            conn.commit()
        return jsonify({'mensaje': 'Pedido enviado con repartidor'})
    finally:
        conn.close()

# 4. Cambiar estatus a 'entregado' (cuando el cliente confirma)
@pedidos_negocio_bp.route('/marcar_entregado/<int:pedido_id>', methods=['POST'])
@jwt_required()
def marcar_entregado(pedido_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Pedidos SET estatus = 'entregado' WHERE id = %s AND negocio_id = %s
            """, (pedido_id, identity))
            conn.commit()
        return jsonify({'mensaje': 'Pedido marcado como entregado'})
    finally:
        conn.close()

# Endpoint para ver todos los pedidos del negocio (historial)
@pedidos_negocio_bp.route('/todos', methods=['GET'])
@jwt_required()
def listar_todos_pedidos():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Pedidos WHERE negocio_id = %s ORDER BY fecha DESC", (identity,))
            pedidos = cursor.fetchall()
        return jsonify({'pedidos': pedidos})
    finally:
        conn.close()

# Endpoint para ver detalles de un pedido específico
@pedidos_negocio_bp.route('/detalle/<int:pedido_id>', methods=['GET'])
@jwt_required()
def detalle_pedido(pedido_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Pedidos WHERE id = %s AND negocio_id = %s", (pedido_id, identity))
            pedido = cursor.fetchone()
        return jsonify({'pedido': pedido})
    finally:
        conn.close()

# Endpoint para cambiar estatus a 'en_camino' (pedido salió para entrega)
@pedidos_negocio_bp.route('/en_camino/<int:pedido_id>', methods=['POST'])
@jwt_required()
def pedido_en_camino(pedido_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Pedidos SET estatus = 'en_camino' WHERE id = %s AND negocio_id = %s
            """, (pedido_id, identity))
            conn.commit()
        return jsonify({'mensaje': 'Pedido marcado como en camino'})
    finally:
        conn.close()
