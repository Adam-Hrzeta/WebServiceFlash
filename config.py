# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

class Config:
    # Configuración de la base de datos
    DB_HOST = '195.179.238.52'
    DB_USER = 'u748254830_flashent_usr'
    DB_PASSWORD = '%%FenT%_2025%%'
    DB_NAME = 'u748254830_flashent_devdb'
    DB_PORT = 3306

    # Configuración de JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'tu-clave-secreta-jwt')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Configuración de la aplicación Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu-clave-secreta-flask')
    DEBUG = True
    ENV = os.getenv('FLASK_ENV', 'production')

    # Configuración de CORS
    CORS_ORIGINS = ['*']  # En producción, especificar los orígenes permitidos

    # Seguridad de contraseñas
    PASSWORD_SALT = os.getenv('PASSWORD_SALT', 'tu-salt-secreto')

    # Configuración de rate limiting
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 60))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 60))  # en segundos
