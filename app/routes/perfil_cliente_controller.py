from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config

cliente_bp = Blueprint('cliente_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@cliente_bp.route('/profileCliente', methods=['GET'])
@jwt_required()
def cliente_profile():
    identity = get_jwt_identity()  # Esto es el id (string)
    claims = get_jwt()             # Aquí están los claims extra

    if not claims or claims.get('tipo_usuario') != 'cliente':
        return jsonify({'error': 'No autorizado'}), 403

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, telefono, correo, fecha_nacimiento FROM Cliente WHERE id = %s", (identity,))
            cliente = cursor.fetchone()
            if not cliente:
                return jsonify({'error': 'Cliente no encontrado'}), 404
            cliente['avatar'] = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
            return jsonify({'cliente': cliente})
    finally:
        conn.close()