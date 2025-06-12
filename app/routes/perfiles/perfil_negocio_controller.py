from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config

perfil_negocio_bp = Blueprint('perfil_negocio_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@perfil_negocio_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de negocio funcionando'
    })

@perfil_negocio_bp.route('/perfilNegocio', methods=['GET'])
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
                "SELECT id, nombre, categoria, telefono, correo, descripcion FROM Negocio WHERE id = %s",
                (identity,)
            )
            negocio = cursor.fetchone()

            if not negocio:
                return jsonify({'error': 'Negocio no encontrado'}), 404

            return jsonify({
                'negocio': negocio
            })
    finally:
        conn.close()

@perfil_negocio_bp.route('/editarPerfil', methods=['PUT'])
@jwt_required()
def editar_perfil_negocio():
    identity = get_jwt_identity()
    claims = get_jwt()

    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json()
    nombre = data.get('nombre')
    categoria = data.get('categoria')
    telefono = data.get('telefono')
    correo = data.get('correo')
    descripcion = data.get('descripcion')

    if not nombre or not categoria or not telefono or not correo or not descripcion:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Negocio SET nombre = %s, categoria = %s, telefono = %s, correo = %s, descripcion = %s WHERE id = %s",
                (nombre, categoria, telefono, correo, descripcion, identity)
            )
            conn.commit()

            # Obtener el perfil actualizado
            cursor.execute(
                "SELECT id, nombre, categoria, telefono, correo, descripcion FROM Negocio WHERE id = %s",
                (identity,)
            )

            negocio = cursor.fetchone()
            if not negocio:
                return jsonify({'error': 'Negocio no encontrado'}), 404
            negocio['avatar'] = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
            return jsonify({'negocio': negocio})
    finally:
        conn.close()
