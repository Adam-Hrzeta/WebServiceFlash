# app/auth.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta
import pymysql
from config import Config
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoginModel(BaseModel):
    usuario: str
    contrasena: str

# Función para conectarse a MySQL
def get_connection():
    return pymysql.connect(
        host=Config.DB_HOST, 
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def is_valid_hash_format(hash_string):
    """Verifica si el hash tiene un formato válido"""
    try:
        if not hash_string.startswith('pbkdf2:sha256:'):
            return False
        return True
    except:
        return False

# Función de login real con base de datos
def login_usuario():
    try:
        data = request.get_json()
        login_data = LoginModel(**data)
        
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Negocio WHERE correo = %s"
            cursor.execute(sql, (login_data.usuario,))
            usuario_guardado = cursor.fetchone()

            if not usuario_guardado:
                return jsonify({
                    "error": "Usuario no encontrado"
                }), 401

            if not is_valid_hash_format(usuario_guardado["contrasena"]):
                logger.error(f"Hash inválido para usuario {login_data.usuario}")
                return jsonify({
                    "error": "Error en el formato de la contraseña almacenada"
                }), 500

            try:
                if check_password_hash(usuario_guardado["contrasena"], login_data.contrasena):
                    token = create_access_token(identity=login_data.usuario, expires_delta=timedelta(hours=1))
                    return jsonify({
                        "mensaje": "Login exitoso",
                        "token": token
                    }), 200
                else:
                    return jsonify({
                        "error": "Credenciales inválidas"
                    }), 401
            except ValueError as e:
                logger.error(f"Error al verificar contraseña: {str(e)}")
                return jsonify({
                    "error": "Error al procesar la contraseña"
                }), 500

    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            connection.close()
        except:
            pass  # Si hubo un error antes de conectar, evitamos otro error aquí
