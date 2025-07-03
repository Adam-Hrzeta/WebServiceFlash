from flask import Blueprint, jsonify, request
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

@perfil_repartidor_bp.route('/upload_profile_image', methods=['POST'])
@jwt_required()
def upload_profile_image_repartidor():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'repartidor':
        return jsonify({'error': 'No autorizado'}), 403
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen'}), 400
    image = request.files['image']
    image_data = image.read()
    if not image_data:
        return jsonify({'error': 'Imagen vacía'}), 400
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE Repartidor SET profile_image = %s WHERE id = %s", (image_data, identity))
            conn.commit()
        return jsonify({'mensaje': 'Imagen de perfil actualizada correctamente'}), 200
    finally:
        conn.close()

@perfil_repartidor_bp.route('/profile_image', methods=['GET'])
def get_profile_image_repartidor():
    user_id = request.args.get('id')
    if not user_id:
        return '', 404
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT profile_image FROM Repartidor WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if not result or not result['profile_image']:
                from flask import send_file
                import io
                return send_file(io.BytesIO(b''), mimetype='image/jpeg')
            from flask import send_file
            import io
            return send_file(io.BytesIO(result['profile_image']), mimetype='image/jpeg')
    finally:
        conn.close()

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
            cursor.execute("SELECT id, nombre, telefono, correo, fecha_nacimiento, tipo_servicio, disponibilidad, profile_image FROM Repartidor WHERE id = %s", (identity,))
            repartidor = cursor.fetchone()
            if not repartidor:
                return jsonify({'error': 'Repartidor no encontrado'}), 404
            if repartidor['profile_image']:
                from flask import request as flask_request
                base_url = flask_request.host_url.rstrip('/')
                repartidor['avatar'] = f"{base_url}/api/perfilRepartidor/profile_image?id={repartidor['id']}"
            else:
                repartidor['avatar'] = None
            del repartidor['profile_image']
            return jsonify({'repartidor': repartidor})
    finally:
        conn.close()

@perfil_repartidor_bp.route('/editarPerfil', methods=['PUT'])
@jwt_required()
def editar_perfil_repartidor():
    identity = get_jwt_identity()
    claims = get_jwt()

    if not claims or claims.get('tipo_usuario') != 'repartidor':
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')

    if not nombre or not correo or not telefono:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Repartidor SET nombre = %s, correo = %s, telefono = %s WHERE id = %s",
                (nombre, correo, telefono, identity)
            )
            conn.commit()
            # Obtener el perfil actualizado
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