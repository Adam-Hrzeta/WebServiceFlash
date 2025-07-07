from app.routes.administracion.blueprints import dashboard_admin_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from config import Config
import pymysql

# Ruta para listar usuarios
@dashboard_admin_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            # Unificar usuarios de todas las tablas
            usuarios = []
            # Administradores
            cursor.execute("SELECT id, nombre, correo, 'administrador' as tipo FROM Administradores")
            usuarios += cursor.fetchall()
            # Clientes
            cursor.execute("SELECT id, nombre, correo, 'cliente' as tipo FROM Cliente")
            usuarios += cursor.fetchall()
            # Negocios
            cursor.execute("SELECT id, nombre, correo, 'negocio' as tipo FROM Negocio")
            usuarios += cursor.fetchall()
            # Repartidores
            cursor.execute("SELECT id, nombre, correo, 'repartidor' as tipo FROM Repartidor")
            usuarios += cursor.fetchall()
        return jsonify(usuarios), 200
    finally:
        conn.close()

# Crear usuario
@dashboard_admin_bp.route('/usuarios', methods=['POST'])
@jwt_required()
def crear_usuario():
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    tipo = data.get('tipo')
    contrasena = data.get('contrasena')
    if not nombre or not correo or not tipo or not contrasena:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400
    tabla = None
    if tipo == 'administrador':
        tabla = 'Administrador'
    elif tipo == 'cliente':
        tabla = 'Cliente'
    elif tipo == 'negocio':
        tabla = 'Negocio'
    elif tipo == 'repartidor':
        tabla = 'Repartidor'
    else:
        return jsonify({'error': 'Tipo de usuario no válido'}), 400
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            # Ajusta los campos según la tabla
            if tabla == 'Administrador':
                cursor.execute("INSERT INTO Administrador (nombre, correo, contrasena, tipo_usuario, telefono) VALUES (%s, %s, %s, %s, '')", (nombre, correo, contrasena, tipo))
            elif tabla == 'Cliente':
                cursor.execute("INSERT INTO Cliente (nombre, correo, contrasena, telefono, direccion) VALUES (%s, %s, %s, '', '')", (nombre, correo, contrasena))
            elif tabla == 'Negocio':
                cursor.execute("INSERT INTO Negocio (nombre, correo, contrasena, telefono, direccion, descripcion, disponibilidad, tipo_entrega, categoria) VALUES (%s, %s, %s, '', '', '', 1, '', '')", (nombre, correo, contrasena))
            elif tabla == 'Repartidor':
                cursor.execute("INSERT INTO Repartidor (nombre, correo, contrasena, telefono, disponibilidad) VALUES (%s, %s, %s, '', 1)", (nombre, correo, contrasena))
            conn.commit()
        return jsonify({'mensaje': f'{tipo.capitalize()} creado'}), 201
    finally:
        conn.close()

# Editar usuario
@dashboard_admin_bp.route('/usuarios/<tipo>/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def editar_usuario(tipo, usuario_id):
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    if not nombre or not correo:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400
    tabla = None
    if tipo == 'administrador':
        tabla = 'Administrador'
    elif tipo == 'cliente':
        tabla = 'Cliente'
    elif tipo == 'negocio':
        tabla = 'Negocio'
    elif tipo == 'repartidor':
        tabla = 'Repartidor'
    else:
        return jsonify({'error': 'Tipo de usuario no válido'}), 400
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            if contrasena:
                cursor.execute(f"UPDATE {tabla} SET nombre=%s, correo=%s, contrasena=%s WHERE id=%s", (nombre, correo, contrasena, usuario_id))
            else:
                cursor.execute(f"UPDATE {tabla} SET nombre=%s, correo=%s WHERE id=%s", (nombre, correo, usuario_id))
            conn.commit()
        return jsonify({'mensaje': f'{tipo.capitalize()} actualizado'}), 200
    finally:
        conn.close()

# Eliminar usuario
@dashboard_admin_bp.route('/usuarios/<tipo>/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario(tipo, usuario_id):
    claims = get_jwt()
    if not claims or claims.get('tipo_usuario') not in ['admin', 'administrador']:
        return jsonify({'error': 'No autorizado'}), 403
    tabla = None
    if tipo == 'administrador':
        tabla = 'Administrador'
    elif tipo == 'cliente':
        tabla = 'Cliente'
    elif tipo == 'negocio':
        tabla = 'Negocio'
    elif tipo == 'repartidor':
        tabla = 'Repartidor'
    else:
        return jsonify({'error': 'Tipo de usuario no válido'}), 400
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM {tabla} WHERE id=%s", (usuario_id,))
            conn.commit()
        return jsonify({'mensaje': f'{tipo.capitalize()} eliminado'}), 200
    finally:
        conn.close()
