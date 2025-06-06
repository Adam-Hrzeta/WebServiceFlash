from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/userType', methods=['GET'])
@jwt_required()
def user_type():
    identity = get_jwt_identity()
    if not identity or 'tipo_usuario' not in identity:
        return jsonify({'error': 'No autenticado', 'status': 'error'}), 401
    return jsonify({'userType': identity['tipo_usuario']}), 200
