from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config

negocio_bp = Blueprint('negocio_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@negocio_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de negocio funcionando'
    })

@negocio_bp.route('/profileNegocio', methods=['GET'])
@jwt_required()
def negocio_profile():
    identity = get_jwt_identity()
    claims = get_jwt()

    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, categoria, telefono, correo, descripcion, cover_photo FROM Negocio WHERE id = %s",
                (identity,)
            )
            negocio = cursor.fetchone()
            if not negocio:
                return jsonify({'error': 'Negocio no encontrado'}), 404
            negocio['avatar'] = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'

            cursor.execute(
                "SELECT id, nombre, descripcion, precio, imagen_url FROM Producto WHERE negocio_id = %s",
                (identity,)
            )
            productos = cursor.fetchall()

            return jsonify({
                'negocio': negocio,
                'productos': productos
            })
    finally:
        conn.close()