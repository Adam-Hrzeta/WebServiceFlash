from flask import Blueprint, jsonify

repartidor_bp = Blueprint('repartidor_bp', __name__)

@repartidor_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de repartidor funcionando'
    })

@repartidor_bp.route('/profileRepartidor', methods=['GET'])
def repartidor_profile():
    repartidor = {
        'id': 1,
        'nombre': 'el fos :P',
        'telefono': '+52 321 456 7890',
        'correo': 'diferente@diferente.com',
        'avatar': 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png',
        'fecha_nacimiento': '1995-01-01',
        'tipo_servicio': 'Cuenta Propia',
        'disponibilidad': 'Disponible',
    }
    return jsonify({
        'repartidor': repartidor
    })
