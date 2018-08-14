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
    """
        Get a list of entries
        First line is the summary
        All following lines until the hyphens is added to description
        ---
        parameters:
           - in: body
        username: body
        description: JSON parameters.
        schema:
          properties:
            username:
              type: string
              description: user name that is used during login.
              example: flintking
            password:
              type: string
              description: password for accessing the entries.
              example: password123
        definitions:
          Entry:
            type: object
            properties:
              entry_id:
                type: string
              entry_date:
                type: string
              title:
                type: string
              description:
                type: string
        responses:
          200:
            description: Returns a list of entries
            schema:
              id: entries
              type: object
              properties:
                entries:
                  type: array
            examples:
              entries: [{"description": "some stuff", "entry date": "02-08-2018",
                        "entry id": 1,"title": "this is a test"}]

        """
    entries = entry_model.get_all_entries_by_id(author_id=current_user)
    output = entry(entries)
    return jsonify({'entries': output}), 200


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
@token_required
def return_one(current_user, entry_id):
    """Example endpoint return a single entry by entry_id
        ---
        parameters:
          - name: entry_id
            in: path
            type: int
            required: true
            default: all
            description: Which entry to filter?
        operationId: get_entry
        consumes:
          - application/json
        produces:
          - application/json

        definitions:
          entries:
            type: object
            properties:
              entry_id:
                type: array
                items:
                  $ref: '#/definitions/entry'
          entry:
            type: string
        responses:
          200:
            description: A list of entries (may be filtered by entry_id)
            schema:
              $ref: '#/definitions/entry'
            examples:
              entries: [{'entry_id':'1', 'entry_date': '20-10-18', 'lorem ipsum'}]
        """
    try:
        entry_details = entry_model.get_single_entry(entry_id)
        output = entry(entry_details)
        return make_response(jsonify({'entry': output[0]}))
    except IndexError:
        return make_response(jsonify({'message': 'the entry you are trying to access does not exist'})), 401


@app.route('/api/v1/entries', methods=['POST'])
@token_required
def add_one(current_user):
    """
        This adds an entry to the list.
        ---
        parameters:
          - in: body
            entry: body
            description: JSON parameters.
            schema:
              properties:
                title:
                  type: string
                  description: title for the new entry
                  example: Alice in wounderland
                description:
                  type: string
                  description: owns description of how his or her day was like.
                  example: what we made it to a new world
        responses:
          201:
            description: OK.
        """
    data = request.get_json()

    # checking if all keys have been provided
    fields = ("title", "description")
    for field in fields:
        if field not in data:
            return jsonify({'error': 'missing ' + field}), 404

    # needed variables for the adding the a new entry
    entry_date = datetime.datetime.today().strftime('%d-%m-%Y')
    title_ = str(data['title']).strip()
    description_ = str(data['description']).strip()
    new_entry = dict(date=entry_date, title=title_, description=description_)

    # first get all entries for that user
    entries = entry_model.get_all_entries_by_id(current_user)
    output = entry(entries)

    # checking if there is a duplicate title in the database
    check_entry = list(filter(lambda output: output['title'] == title_, output))
    if check_entry == []:
        if title_ is "" or description_ is "":
            return jsonify({'message': " fields can not be empty"}), 404
        else:
            entry_model.insert_new_entry(new_date=entry_date, title=title_,
                                         description=description_,
                                         author_id=current_user
                                         )
            return jsonify({'entry': new_entry, 'message': "New entry added"}), 201
    else:
        return jsonify({'message ': 'title already exists'}), 401


@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
@token_required
def edit_one(current_user, entry_id):
    """
        This adds an entry to the list.
        ---
        parameters:
          - in: body
            entry: body
            description: JSON parameters.
            schema:
              properties:
                title:
                  type: string
                  description: title for the new entry
                  example: Alice in wounderland
                description:
                  type: string
                  description: owns description of how his or her day was like.
                  example: what we made it to a new world
        responses:
          201:
            description: OK.
        """
    data = request.get_json()
    entry_date = datetime.datetime.today().strftime('%d-%m-%Y')
    entries = entry_model.get_single_entry(entry_id)
    output = entry(entries)
    check_entry = list(filter(lambda output: output['entry date'] == entry_date, output))
    print(check_entry)
    # checking if the entry is being edited on the same day
    if check_entry is not []:
        entry_model.update_single_data(data['title'], data['description'], entry_id)
        return jsonify(dict(output=output[0], message='entry updated')), 201
    else:
        return jsonify(dict(message='you can only edit an entry on the day it was created'))

