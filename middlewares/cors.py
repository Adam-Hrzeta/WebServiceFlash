from flask_cors import CORS

def configure_cors(app):
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],  # Ajustar según el frontend
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Range", "X-Content-Range"],
            "supports_credentials": True,
            "max_age": 600
        }
    }) 