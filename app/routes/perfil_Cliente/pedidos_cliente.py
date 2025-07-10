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
    direccion_entrega = data.get('direccion_entrega')
    cliente_id = get_jwt_identity()
    if not productos or not cliente_id or not negocio_id or not direccion_entrega:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Pedidos (cliente_id, negocio_id, total, fecha, direccion_entrega) VALUES (%s, %s, %s, NOW(), %s)",
                (cliente_id, negocio_id, total, direccion_entrega)
            )
            pedido_id = cursor.lastrowid

            # Insertar productos en detalle_pedido (acepta producto_id o id, y precio_unitario o precio)
            for prod in productos:
                producto_id = prod.get('producto_id') or prod.get('id')
                cantidad = prod.get('cantidad')
                precio_unitario = prod.get('precio_unitario') or prod.get('precio')
                if not producto_id or cantidad is None or precio_unitario is None:
                    print(f"[ERROR] Producto inválido: {prod}")
                    continue
                cursor.execute(
                    "INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                    (pedido_id, producto_id, cantidad, precio_unitario)
                )
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
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    print('JWT claims recibidos (historial):', claims)
    if not claims or claims.get('tipo_usuario') != 'cliente':
        print('Acceso denegado. Claims:', claims)
        return jsonify({'status': 'error', 'mensaje': 'No autorizado'}), 403
    cliente_id = get_jwt_identity()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.negocio_id, n.nombre AS negocio_nombre, p.total, p.fecha, p.estatus, p.direccion_entrega
                FROM Pedidos p
                JOIN Negocio n ON p.negocio_id = n.id
                WHERE p.cliente_id = %s
                ORDER BY p.fecha DESC
            """, (cliente_id,))
            pedidos = cursor.fetchall()
            # Para cada pedido, obtener los productos asociados
            for pedido in pedidos:
                cursor.execute("""
                    SELECT d.producto_id, pr.nombre, d.cantidad, d.precio_unitario
                    FROM detalle_pedido d
                    JOIN Productos pr ON d.producto_id = pr.id
                    WHERE d.pedido_id = %s
                """, (pedido['id'],))
                productos = cursor.fetchall()
                pedido['productos'] = productos
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
