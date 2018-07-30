from flask import jsonify, request, make_response

from api import app


entries = [
    {"entry_id": 1, "date": "21/07/2017",
     "title": "jonathan in never land", "description": "lorem ipsum"},
    {"entry_id": 2, "date": "21/07/2017",
     "title": "jonathan in never land", "description": "lorem ipsum"},
    {"entry_id": 3, "date": "21/07/2017",
     "title": "leader are made not born", "description": "lorem ipsum"},
    {"entry_id": 4, "date": "21/07/2017",
     "title": "we are all special in every way", "description": "lorem ipsum"}]


@app.route('/')
def index():
    return jsonify({'message': "Welcome to the entry port"})


@app.route('/api/v1/entries', methods=['GET'])
def return_all():
    return jsonify({'entries': entries})


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
def return_one(entry_id):
    """ end point for displaying a single item """

    entry = [entry for entry in entries if entry["entry_id"] == entry_id]
    return make_response(jsonify({'entry': entry[0]}))


@app.route('/api/v1/entries', methods=['POST'])
def add_one():
    """ end point for adding items to the entries """
    next_id = len(entries)
    new_id = int(next_id+1)
    new_entry = {
        'entry_id': new_id,
        'date': request.json["date"],
        'title': request.json["title"],
        'description': request.json["description"]}
    # if new_entry['title'] or new_entry['date'] or new_entry['description'] is None:
    #     return make_response(jsonify({'message': "fields must not be empty"}),404)
    entries.append(new_entry)
    response=jsonify({'message': "New entry added"})
    response.status_code=201
    return response
    # return make_response(jsonify({'message': "New entry added"}), 201)


@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
def edit_one(entry_id):
    """  end point for modifying the entries """

    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    entry[0]['title'] = request.json['title']
    entry[0]['description'] = request.json['description']
    if entry[0]['title'] or entry[0]['description'] is None:
        return jsonify({'message': "fields must not be empty"})
    return jsonify(dict(entry=entry[0]))


@app.route('/api/v1/entries/<int:entry_id>', methods=['Delete'])
def delete_one(entry_id):
    """ end point for deleting an item """

    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    if entry[0] is None:
        return jsonify({'message': 'entry not found'})
    entries.remove(entry[0])
    return jsonify({'message': "deleted"})
