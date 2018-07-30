from flask import jsonify, request, make_response
from utils import token_required, entry
import db
from config import db_connection as conn
from api import app
import datetime


@app.route('/')
def index():
    return jsonify({'message': "Welcome to the entry port"})


@app.route('/api/v1/entries', methods=['GET'])
@token_required
def return_all(current_user):
    entries = db.get_all_entries(conn, author_id=current_user)
    output = entry(entries)
    return jsonify({'entries': output}), 200


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
@token_required
def return_one(current_user, entry_id):
    """ end point for displaying a single item """
    entry_details = db.get_single_entry(conn, entry_id)
    output = entry(entry_details)
    return make_response(jsonify({'entry': output}))


@app.route('/api/v1/entries', methods=['POST'])
@token_required
def add_one(current_user):
    """ end point for adding items to the entries """
    data = request.get_json()
    entry_date = datetime.datetime.today().strftime('%d-%m-%Y')
    title_ = data['title']
    description_ = data['description']
    db.insert_new_entry(conn, new_date=entry_date, title=title_, description=description_,
                        author_id=current_user)
    return jsonify({'message': "New entry added"}), 201


@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
@token_required
def edit_one(current_user, entry_id):
    """  end point for modifying the entries """
    data = request.get_json()
    db.update_single_data(conn, data['title'], data['description'], entry_id)
    return jsonify(dict(message='entry updated'))


# @app.route('/api/v1/entries/<int:entry_id>', methods=['Delete'])
# def delete_one(entry_id):
#     """ end point for deleting an item """
#
#     entry = check_entry(entry_id)
#     entries.remove(entry[0])
#     return jsonify({'message': "deleted"})


# def check_entry(entry_id):
#     entry = []
#     for entry in entries:
#         if entry['entry_id'] == entry_id:
#             entry.append(entry)
#     return entry
