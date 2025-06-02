from flask import Flask
from flask_cors import CORS
import mysql.connector
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Conexión a la base de datos
    def get_db_connection():
        return mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )

    # Guardamos la función para que puedas usarla en rutas
    app.get_db_connection = get_db_connection

    # Esto es solo si ya tienes un archivo routes/api.py con un Blueprint
    try:
        from .routes import api
        app.register_blueprint(api)
    except ImportError:
        pass  # Si no tienes rutas todavía, lo ignoramos

    return app


# Solo para probar conexión si ejecutas test_db.py directamente
if __name__ == '__main__':
    try:
        conexion = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )
        if conexion.is_connected():
            print("✅ ¡Conectado a MySQL exitosamente!")
            conexion.close()
    except Exception as e:
        print("❌ Error al conectar:", e)
