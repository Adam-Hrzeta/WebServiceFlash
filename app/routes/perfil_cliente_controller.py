from flask import Blueprint, jsonify

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de cliente funcionando'
    })

@cliente_bp.route('/profileCliente', methods=['GET'])
def cliente_profile():
    cliente = {
        'id': 1,
        'nombre': 'la ester :P',
        'telefono': '+52 123 456 7890',
        'correo': 'prueba@prueba.com',
        'avatar': 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png',
        'fecha_nacimiento': '2000-01-01',
    }
    return jsonify({
        'cliente': cliente
    })
