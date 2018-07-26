from flask import jsonify, request, make_response
from utils import token_required
from db import insert_new_entry,get_all_entries, get_single_entry,update_single_data
from config import db_connection as conn
from api import app


# entries = [
#     {"entry_id": 1, "date": "21/07/2017", "title": "jonathan in never land", "description": "lorem ipsum"},
#     {"entry_id": 2, "date": "21/07/2017", "title": "jonathan in never land", "description": "lorem ipsum"},
#     {"entry_id": 3, "date": "21/07/2017", "title": "leader are made not born", "description": "lorem ipsum"},
#     {"entry_id": 4, "date": "21/07/2017", "title": "we are all special in every way", "description": "lorem ipsum"}]


@app.route('/')
def index():
    return jsonify({'message': "Welcome to the entry port"})


@app.route('/api/v1/entries', methods=['GET'])
@token_required
def return_all(current_user):
    entries = get_all_entries(conn, author_id=current_user)
    output = []
    for entry in entries:
        user_data = {' entry id': entry[1], 'title': entry[2], 'description': entry[3]}
        output.append(user_data)
    return jsonify({'entries': output}),200


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
@token_required
def return_one(current_user, entry_id):
    """ end point for displaying a single item """
    entry_details=get_single_entry(conn,entry_id)
    output = []
    for entry in entry_details:
        user_data = {' Date ': entry[1], 'title': entry[2], 'description': entry[3]}
        output.append(user_data)
    return make_response(jsonify({'entry': output}))


@app.route('/api/v1/entries', methods=['POST'])
@token_required
def add_one(current_user):
    """ end point for adding items to the entries """
    data = request.get_json()
    insert_new_entry(conn, new_date=data['date'], title=data['title'], description=data['description'],
                     author_id=current_user)
    return jsonify({'message': "New entry added"}), 201


@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
@token_required
def edit_one(current_user,entry_id):
    """  end point for modifying the entries """
    data=request.get_json()
    update_single_data(conn, data['title'],data['description'], entry_id)

    return jsonify(dict(message='entry updated'))


@app.route('/api/v1/entries/<int:entry_id>', methods=['Delete'])
def delete_one(entry_id):
    """ end point for deleting an item """

    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    entries.remove(entry[0])
    return jsonify({'message': "deleted"})
