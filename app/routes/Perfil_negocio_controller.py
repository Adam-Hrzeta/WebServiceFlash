from flask import Blueprint, jsonify

negocio_bp = Blueprint('negocio_bp', __name__)

@negocio_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de negocio funcionando'
    })

@negocio_bp.route('/profileNegocio', methods=['GET'])
def negocio_profile():
    negocio = {
        'id': 1,
        'nombre': 'FlashEnt Pizza',
        'categoria': 'Restaurante',
        'telefono': '+52 123 456 7890',
        'correo': 'flashent@pizza.com',
        'descripcion': 'La mejor pizza de la ciudad',
        'cover_photo': 'https://via.placeholder.com/400x150',
        'avatar': 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png',
    }
    productos = [
        {
            'id': 1,
            'nombre': 'Pizza Margarita',
            'descripcion': 'Clásica pizza con tomate y albahaca',
            'precio': 120.0,
            'imagen_url': 'https://via.placeholder.com/150'
        },
        {
            'id': 2,
            'nombre': 'Pizza Pepperoni',
            'descripcion': 'Con mucho pepperoni',
            'precio': 140.0,
            'imagen_url': 'https://via.placeholder.com/150'
        },
        {
            'id': 3,
            'nombre': 'Pizza Vegetariana',
            'descripcion': 'Con vegetales frescos',
            'precio': 130.0,
            'imagen_url': 'https://via.placeholder.com/150'
        }
    ]
    return jsonify({
        'negocio': negocio,
        'productos': productos
    })
