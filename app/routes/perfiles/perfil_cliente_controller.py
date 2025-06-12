from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config

perfil_cliente_bp = Blueprint('perfil_cliente_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@perfil_cliente_bp.route('/perfilCliente', methods=['GET'])
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

@perfil_cliente_bp.route('/editarPerfil', methods=['PUT'])
@jwt_required()
def editar_perfil_cliente():
    identity = get_jwt_identity()
    claims = get_jwt()

    if not claims or claims.get('tipo_usuario') != 'cliente':
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    fecha_nacimiento = data.get('fecha_nacimiento')

    if not nombre or not correo or not telefono or not fecha_nacimiento:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Cliente SET nombre = %s, correo = %s, telefono = %s, fecha_nacimiento = %s WHERE id = %s",
                (nombre, correo, telefono, fecha_nacimiento, identity)
            )
            conn.commit()
            cursor.execute("SELECT id, nombre, telefono, correo, fecha_nacimiento FROM Cliente WHERE id = %s", (identity,))
            cliente = cursor.fetchone()
            if not cliente:
                return jsonify({'error': 'Cliente no encontrado'}), 404
            cliente['avatar'] = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
            return jsonify({'cliente': cliente})
    finally:
        conn.close()