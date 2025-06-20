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

@perfil_negocio_bp.route('/upload_profile_image', methods=['POST'])
@jwt_required()
def upload_profile_image_negocio():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
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
            cursor.execute("UPDATE Negocio SET profile_image = %s WHERE id = %s", (image_data, identity))
            conn.commit()
        return jsonify({'mensaje': 'Imagen de perfil actualizada correctamente'}), 200
    finally:
        conn.close()

@perfil_negocio_bp.route('/profile_image', methods=['GET'])
def get_profile_image_negocio():
    user_id = request.args.get('id')
    if not user_id:
        return '', 404
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT profile_image FROM Negocio WHERE id = %s", (user_id,))
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
            cursor.execute("SELECT id, nombre, categoria, telefono, correo, descripcion, direccion, profile_image FROM Negocio WHERE id = %s", (identity,))
            negocio = cursor.fetchone()

            if not negocio:
                return jsonify({'error': 'Negocio no encontrado'}), 404

            if negocio['profile_image']:
                from flask import request as flask_request
                base_url = flask_request.host_url.rstrip('/')
                negocio['avatar'] = f"{base_url}/api/perfilNegocio/profile_image?id={negocio['id']}"
            else:
                negocio['avatar'] = None

            del negocio['profile_image']

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
