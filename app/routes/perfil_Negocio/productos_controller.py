from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import pymysql
from config import Config
from datetime import datetime
import io

productos_bp = Blueprint('productos_bp', __name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Obtener todos los productos del negocio autenticado
@productos_bp.route('/', methods=['GET'])
@jwt_required()
def get_productos():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, categoria, stock, fecha_creacion FROM Productos WHERE negocio_id = %s", (identity,))
            productos = cursor.fetchall()
            # Agregar imagen_url a cada producto
            for producto in productos:
                producto['imagen_url'] = f"/api/productos/{producto['id']}/imagen"
        return jsonify(productos), 200
    finally:
        conn.close()

# Crear un producto
@productos_bp.route('/', methods=['POST'])
@jwt_required()
def create_producto():
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    data = request.form
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    categoria = data.get('categoria')
    stock = data.get('stock', 0)
    imagen = request.files.get('imagen')
    imagen_data = imagen.read() if imagen else None
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Productos (negocio_id, nombre, descripcion, precio, categoria, stock, imagen, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (identity, nombre, descripcion, precio, categoria, stock, imagen_data, datetime.now()))
            conn.commit()
        return jsonify({'mensaje': 'Producto creado exitosamente'}), 201
    finally:
        conn.close()

# Obtener imagen de producto
@productos_bp.route('/<int:producto_id>/imagen', methods=['GET'])
def get_producto_imagen(producto_id):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT imagen FROM Productos WHERE id = %s", (producto_id,))
            result = cursor.fetchone()
            if not result or not result['imagen']:
                return '', 404
            return send_file(io.BytesIO(result['imagen']), mimetype='image/jpeg')
    finally:
        conn.close()

# Actualizar producto
@productos_bp.route('/<int:producto_id>', methods=['PUT'])
@jwt_required()
def update_producto(producto_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    data = request.form
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    categoria = data.get('categoria')
    stock = data.get('stock', 0)
    imagen = request.files.get('imagen')
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            if imagen:
                imagen_data = imagen.read()
                cursor.execute("""
                    UPDATE Productos SET nombre=%s, descripcion=%s, precio=%s, categoria=%s, stock=%s, imagen=%s WHERE id=%s AND negocio_id=%s
                """, (nombre, descripcion, precio, categoria, stock, imagen_data, producto_id, identity))
            else:
                cursor.execute("""
                    UPDATE Productos SET nombre=%s, descripcion=%s, precio=%s, categoria=%s, stock=%s WHERE id=%s AND negocio_id=%s
                """, (nombre, descripcion, precio, categoria, stock, producto_id, identity))
            conn.commit()
        return jsonify({'mensaje': 'Producto actualizado correctamente'}), 200
    finally:
        conn.close()

# Eliminar producto
@productos_bp.route('/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def delete_producto(producto_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') != 'negocio':
        return jsonify({'error': 'No autorizado'}), 403
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Productos WHERE id = %s AND negocio_id = %s", (producto_id, identity))
            conn.commit()
        return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200
    finally:
        conn.close()
