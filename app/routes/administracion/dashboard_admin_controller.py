from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
import pymysql
from config import Config

dashboard_admin_bp = Blueprint('dashboard_admin_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Listar negocios pendientes
@dashboard_admin_bp.route('/negocios_pendientes', methods=['GET'])
@jwt_required()
def listar_negocios_pendientes():
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Negocio WHERE estado = 'pendiente'")
            negocios = cursor.fetchall()
            # Excluir campos binarios (como profile_image)
            for n in negocios:
                if 'profile_image' in n:
                    n.pop('profile_image')
        return jsonify(negocios), 200
    finally:
        conn.close()

# Listar repartidores pendientes
@dashboard_admin_bp.route('/repartidores_pendientes', methods=['GET'])
@jwt_required()
def listar_repartidores_pendientes():
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Repartidor WHERE estado = 'pendiente'")
            repartidores = cursor.fetchall()
            # Excluir campos binarios si existieran
            for r in repartidores:
                for k, v in list(r.items()):
                    if isinstance(v, (bytes, bytearray)):
                        r.pop(k)
        return jsonify(repartidores), 200
    finally:
        conn.close()

# Aprobar negocio
@dashboard_admin_bp.route('/aprobar_negocio/<int:negocio_id>', methods=['POST'])
@jwt_required()
def aprobar_negocio(negocio_id):
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE Negocio SET estado = 'aprobado' WHERE id = %s", (negocio_id,))
            conn.commit()
        return jsonify({'mensaje': 'Negocio aprobado'}), 200
    finally:
        conn.close()

# Rechazar negocio
@dashboard_admin_bp.route('/rechazar_negocio/<int:negocio_id>', methods=['POST'])
@jwt_required()
def rechazar_negocio(negocio_id):
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Negocio WHERE id = %s", (negocio_id,))
            conn.commit()
        return jsonify({'mensaje': 'Negocio rechazado y eliminado'}), 200
    finally:
        conn.close()

# Aprobar repartidor
@dashboard_admin_bp.route('/aprobar_repartidor/<int:repartidor_id>', methods=['POST'])
@jwt_required()
def aprobar_repartidor(repartidor_id):
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE Repartidor SET estado = 'aprobado' WHERE id = %s", (repartidor_id,))
            conn.commit()
        return jsonify({'mensaje': 'Repartidor aprobado'}), 200
    finally:
        conn.close()

# Rechazar repartidor
@dashboard_admin_bp.route('/rechazar_repartidor/<int:repartidor_id>', methods=['POST'])
@jwt_required()
def rechazar_repartidor(repartidor_id):
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Repartidor WHERE id = %s", (repartidor_id,))
            conn.commit()
        return jsonify({'mensaje': 'Repartidor rechazado y eliminado'}), 200
    finally:
        conn.close()
