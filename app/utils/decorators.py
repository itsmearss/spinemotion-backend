from functools import wraps
from flask import request, jsonify
from app import jwt, db


def api_key_required(func):
    @wraps(func)
    def check_api_key(*args, **kwargs):
        apiKey = request.headers.get('x-api-key')
        # Logika untuk memeriksa API key
        try:
            db_api_key = db.db.api_key.find_one({"api_key": apiKey})
            print(db_api_key)
            if apiKey == db_api_key["api_key"]:
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "Please provide a correct API key"}), 400
        except Exception as e:
            return {
                "message": "Tidak ada token"
            }, 500
            
    return check_api_key


