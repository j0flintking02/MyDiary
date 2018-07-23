from flask import Flask, jsonify, request, abort


app = Flask(__name__)

entries = [
    {"entry_id": 1, "title": "jonathan in never land", "description": "lorem ipsum"},
    {"entry_id": 2, "title": "jonathan in never land", "description": "lorem ipsum"},
    {"entry_id": 3, "title": "leader are made not born", "description": "lorem ipsum"},
    {"entry_id": 4, "title": "we are all special in every way", "description": "lorem ipsum"}]


@app.route('/')
def index():
    return 'hello world'


@app.route('/api/v1/entries', methods=['GET'])
def return_all():
    return jsonify({'entries': entries})


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
def return_one(entry_id):
    """ end point for displaying a single item """
    if not isinstance(entry_id, int):
        raise ValueError("the value must be an int")

    if entry_id is None:
        abort(404)

    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    return jsonify({'entry': entry[0]})


@app.route('/api/v1/entries', methods=['POST'])
def add_one():
    """ end point for adding items to the entries """
    new_entry = dict(entryId=request.json["entryId"], title=request.json["title"],
                     description=request.json["description"])

    if not all(new_entry.get('entryId')):
        pass
    entries.append(new_entry)
    return jsonify({"entries": entries})


@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
def edit_one(entry_id):
    """  end point for modifying the entries """
    
    if entry_id is None:
        abort(404)

    entry = [entry for entry in entries if entry['entryId'] == entry_id]
    entry[0]['entryId'] = request.json['entryId']
    return jsonify(dict(entry=entry[0]))


@app.route('/api/v1/entries/<int:entry_id>', methods=['Delete'])
def delete_one(entry_id):
    """ end point for deleting an item """
    
    if entry_id is None:
        abort(404)

    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    entries.remove(entry[0])
    return jsonify({'entries': entries})


@app.errorhandler(404)
def not_found(e):
    return '', 404


if __name__ == '__main__':
    app.run(debug=True)
