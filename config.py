# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # Configuración de la base de datos de MySQL
    DB_HOST = '195.179.238.52' #HOST
    DB_USER = 'u748254830_flashent_usr' #USUARIO
    DB_PASSWORD = '%%FenT%_2025%%' #CONTRASEÑA
    DB_NAME = 'u748254830_flashent_devdb' #NOMBRE DE LA BASE DE DATOS
    DB_PORT = 3306 #PUERTO

    # Configuración de JWT PARA LA AUTENTICACIÓN DE LOS USUARIOS
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'tu-clave-secreta-jwt')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) # Tiempo de expiración del token de acceso
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30) # Tiempo de expiración del token de actualización

    # Configuración de la aplicación Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu-clave-secreta-flask') 
    DEBUG = True   # Habilitar el modo de depuración (cambiar a False en producción)
    ENV = os.getenv('FLASK_ENV', 'production') # Entorno de la aplicación (producción o desarrollo)

    # Configuración de CORS
    CORS_ORIGINS = ['*']  # En producción, especificar los orígenes permitidos

    # Seguridad de contraseñas
    PASSWORD_SALT = os.getenv('PASSWORD_SALT', 'tu-salt-secreto')

    # Configuración EL NUMERO DE PETICIONES POR MINUTO 60 REQUEST/PETICIONES POR MINUTO/ 60 SEGUNDOS
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 60)) 
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 60))  # en segundos
