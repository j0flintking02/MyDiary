from flask import jsonify, request, make_response
from utils import token_required, entry
from db import Entries
from api import app
import datetime

entry_model = Entries()


@app.route('/')
def index():
    return jsonify({'message': "Welcome to the entry port"})


@app.route('/api/v1/entries', methods=['GET'])
@token_required
def return_all(current_user):
    entries = entry_model.get_all_entries(author_id=current_user)
    output = entry(entries)
    return jsonify({'entries': output}), 200


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
@token_required
def return_one(current_user, entry_id):
    """ end point for displaying a single item """
    entry_details = entry_model.get_single_entry(entry_id)
    output = entry(entry_details)
    return make_response(jsonify({'entry': output[0]}))


@app.route('/api/v1/entries', methods=['POST'])
@token_required
def add_one(current_user):
    """ end point for adding items to the entries """
    data = request.get_json()
    entry_date = datetime.datetime.today().strftime('%d-%m-%Y')
    title_ = str(data['title']).strip()
    description_ = str(data['description']).strip()
    new_entry = dict(date=entry_date, title=title_, description=description_)
    if title_ is "" or description_ is "":
        return jsonify({'message': " fields can not be empty"}), 404
    entry_model.insert_new_entry(new_date=entry_date, title=title_, description=description_,
                                 author_id=current_user)
    return jsonify({'entry': new_entry, 'message': "New entry added"}), 201


@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
@token_required
def edit_one(current_user, entry_id):
    """  end point for modifying the entries """
    data = request.get_json()
    entry_model.update_single_data(data['title'], data['description'], entry_id)
    return jsonify(dict(message='entry updated'))
