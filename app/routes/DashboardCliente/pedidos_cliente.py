from flask import Blueprint, request, jsonify
from app.models.model_pedido import PedidoCreate, DetallePedido
from flask_jwt_extended import jwt_required, get_jwt_identity
import pymysql
from config import Config

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
    cliente_id = get_jwt_identity()
    if not productos or not cliente_id:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pedidos (cliente_id, total, fecha) VALUES (%s, %s, NOW())",
                (cliente_id, total)
            )
            pedido_id = cursor.lastrowid
            for prod in productos:
                cursor.execute(
                    "INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                    (pedido_id, prod['id'], prod['cantidad'], prod['precio'])
                )
        conn.commit()
        return jsonify({'status': 'success', 'pedido_id': pedido_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()
