from flask import jsonify
from typing import Any, Dict, Optional

def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> tuple:
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message: str = "Error", status_code: int = 400, errors: Optional[Dict] = None) -> tuple:
    response = {
        "success": False,
        "message": message,
        "errors": errors
    }
    return jsonify(response), status_code 