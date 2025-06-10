from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config

perfil_repartidor_bp = Blueprint('perfil_repartidor_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@perfil_repartidor_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de repartidor funcionando'
    })

@perfil_repartidor_bp.route('/perfilRepartidor', methods=['GET'])
@jwt_required()
def repartidor_profile():
    identity = get_jwt_identity()
    claims = get_jwt()

    if not claims or claims.get('tipo_usuario') != 'repartidor':
        return jsonify({'error': 'No autorizado'}), 403

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, telefono, correo, fecha_nacimiento, tipo_servicio, disponibilidad FROM Repartidor WHERE id = %s",
                (identity,)
            )
            repartidor = cursor.fetchone()
            if not repartidor:
                return jsonify({'error': 'Repartidor no encontrado'}), 404
            repartidor['avatar'] = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
            return jsonify({'repartidor': repartidor})
    finally:
        conn.close()