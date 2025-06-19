from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config

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
                SELECT p.id, c.nombre AS cliente_nombre, c.telefono AS cliente_telefono,
                       n.nombre AS negocio_nombre, n.telefono AS negocio_telefono, n.categoria
                FROM Pedido p
                JOIN Cliente c ON p.cliente_id = c.id
                JOIN Negocio n ON p.negocio_id = n.id
                WHERE p.repartidor_id = %s
            """, (identity,))
            pedidos = cursor.fetchall()
            return jsonify({'pedidos': pedidos})
    finally:
        conn.close()
