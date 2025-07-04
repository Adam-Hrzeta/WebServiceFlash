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
            cursor.execute("SELECT id, nombre, categoria, telefono, correo, descripcion, direccion, disponibilidad, profile_image FROM Negocio WHERE id = %s", (identity,))
            negocio = cursor.fetchone()

            if not negocio:
                return jsonify({'error': 'Negocio no encontrado'}), 404

            # Convertir disponibilidad a booleano
            if 'disponibilidad' in negocio:
                negocio['disponibilidad'] = bool(negocio['disponibilidad'])

            if negocio['profile_image']:
                from flask import request as flask_request
                base_url = flask_request.host_url.rstrip('/')
                negocio['avatar'] = f"{base_url}/api/negocio/profile_image?id={negocio['id']}"
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
    # Obtener el perfil actual
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nombre, categoria, telefono, correo, descripcion, direccion, disponibilidad FROM Negocio WHERE id = %s", (identity,))
            actual = cursor.fetchone()
            if not actual:
                return jsonify({'error': 'Negocio no encontrado'}), 404
            # Usar los datos recibidos o los actuales si no se envían
            nombre = data.get('nombre', actual['nombre'])
            categoria = data.get('categoria', actual['categoria'])
            telefono = data.get('telefono', actual['telefono'])
            correo = data.get('correo', actual['correo'])
            descripcion = data.get('descripcion', actual['descripcion'])
            direccion = data.get('direccion', actual['direccion'])
            disponibilidad = data.get('disponibilidad', actual['disponibilidad'])
            cursor.execute(
                "UPDATE Negocio SET nombre = %s, categoria = %s, telefono = %s, correo = %s, descripcion = %s, direccion = %s, disponibilidad = %s WHERE id = %s",
                (nombre, categoria, telefono, correo, descripcion, direccion, disponibilidad, identity)
            )
            conn.commit()
            cursor.execute(
                "SELECT id, nombre, categoria, telefono, correo, descripcion, direccion, disponibilidad FROM Negocio WHERE id = %s",
                (identity,)
            )
            negocio = cursor.fetchone()
            if not negocio:
                return jsonify({'error': 'Negocio no encontrado'}), 404
            negocio['avatar'] = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
            # Convertir disponibilidad a booleano
            if 'disponibilidad' in negocio:
                negocio['disponibilidad'] = bool(negocio['disponibilidad'])
            return jsonify({'negocio': negocio})
    finally:
        conn.close()

@perfil_negocio_bp.route('/solicitudes_aliados', methods=['GET'])
@jwt_required()
def solicitudes_aliados():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.id, s.repartidor_id, r.nombre AS repartidor_nombre, s.estatus, s.fecha
                FROM SolicitudAliado s
                JOIN Repartidor r ON s.repartidor_id = r.id
                WHERE s.negocio_id = %s
                ORDER BY s.fecha DESC
            """, (identity,))
            solicitudes = cursor.fetchall()
        return jsonify({'solicitudes': solicitudes})
    finally:
        conn.close()

@perfil_negocio_bp.route('/solicitud_aliado/<int:solicitud_id>/<accion>', methods=['POST'])
@jwt_required()
def accion_solicitud_aliado(solicitud_id, accion):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    if accion not in ['aceptar', 'rechazar']:
        return jsonify({'error': 'Acción inválida'}), 400
    nuevo_estatus = 'aceptada' if accion == 'aceptar' else 'rechazada'
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE SolicitudAliado SET estatus = %s WHERE id = %s AND negocio_id = %s",
                (nuevo_estatus, solicitud_id, identity)
            )
            conn.commit()
        return jsonify({'mensaje': f'Solicitud {nuevo_estatus}'})
    finally:
        conn.close()
