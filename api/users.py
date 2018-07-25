from flask import jsonify, request

from api import app

user_details = [
    {"user_id": 1, "user_name": "flintKing", "user_password": "1234"},
    {"user_id": 2, "user_name": "JohnDoe", "user_password": "1234"},
    {"user_id": 3, "user_name": "JaneDoe", "user_password": "1234"}
]


@app.route('/api/v1/users', methods=['GET'])
def return_all():
    return jsonify({'details': user_details})


@app.route('/api/v1/users', methods=['GET'])
def return_all():
    return jsonify({'details': user_details})


@app.route('/api/v1/users', methods=['GET'])
def return_all():
    return jsonify({'details': user_details})


@app.route('/api/v1/users', methods=['GET'])
def return_all():
    return jsonify({'details': user_details})
