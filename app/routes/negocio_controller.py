from flask import Blueprint, jsonify

negocio_bp = Blueprint('negocio_bp', __name__)

@negocio_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'mensaje': 'Ruta de negocio funcionando'
    })
