from flask import Blueprint, request, jsonify
from app.models.model_pedido import PedidoCreate, DetallePedido
import pymysql
from config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity

pedidos_cliente_bp = Blueprint('pedidos_cliente', __name__)

def get_db_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

@pedidos_cliente_bp.route('/realizar_pedido', methods=['POST'])
@jwt_required()
def realizar_pedido():
    data = request.get_json()
    productos = data.get('productos', [])
    total = data.get('total', 0)
    negocio_id = data.get('negocio_id')
    cliente_id = get_jwt_identity()
    print(f"[DEBUG] negocio_id recibido: {negocio_id}, cliente_id: {cliente_id}")
    if not productos or not cliente_id or not negocio_id:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Pedidos (cliente_id, negocio_id, total, fecha) VALUES (%s, %s, %s, NOW())",
                (cliente_id, negocio_id, total)
            )
            pedido_id = cursor.lastrowid
            print(f"[DEBUG] Pedido insertado con id: {pedido_id} para negocio_id: {negocio_id}")
        conn.commit()
        return jsonify({'status': 'success', 'pedido_id': pedido_id})
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@pedidos_cliente_bp.route('/historial', methods=['GET'])
@jwt_required()
def historial_pedidos():
    cliente_id = get_jwt_identity()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Pedidos WHERE cliente_id = %s ORDER BY fecha DESC", (cliente_id,))
            pedidos = cursor.fetchall()
        return jsonify({'pedidos': pedidos})
    finally:
        conn.close()

@pedidos_cliente_bp.route('/confirmar_entrega/<int:pedido_id>', methods=['POST'])
@jwt_required()
def confirmar_entrega(pedido_id):
    cliente_id = get_jwt_identity()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Pedidos SET estatus = 'entregado' WHERE id = %s AND cliente_id = %s
            """, (pedido_id, cliente_id))
            conn.commit()
        return jsonify({'mensaje': 'Pedido confirmado como entregado'})
    finally:
        conn.close()
