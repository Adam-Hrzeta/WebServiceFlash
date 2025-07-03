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

@perfil_cliente_bp.route('/upload_profile_image', methods=['POST'])
@jwt_required()
def upload_profile_image_cliente():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'cliente':
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
            cursor.execute("UPDATE Cliente SET profile_image = %s WHERE id = %s", (image_data, identity))
            conn.commit()
        return jsonify({'mensaje': 'Imagen de perfil actualizada correctamente'}), 200
    finally:
        conn.close()

@perfil_cliente_bp.route('/profile_image', methods=['GET'])
def get_profile_image_cliente():
    user_id = request.args.get('id')
    if not user_id:
        return '', 404
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT profile_image FROM Cliente WHERE id = %s", (user_id,))
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
            cursor.execute("SELECT id, nombre, telefono, correo, fecha_nacimiento, profile_image FROM Cliente WHERE id = %s", (identity,))
            cliente = cursor.fetchone()
            if not cliente:
                return jsonify({'error': 'Cliente no encontrado'}), 404
            if cliente['profile_image']:
                from flask import request as flask_request
                base_url = flask_request.host_url.rstrip('/')
                cliente['avatar'] = f"{base_url}/api/perfilCliente/profile_image?id={cliente['id']}"
            else:
                cliente['avatar'] = None
            del cliente['profile_image']
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