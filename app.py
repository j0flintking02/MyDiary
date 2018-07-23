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
    new_entry = {'entry_Id': request.json["entry_id"], 'title': request.json["title"],
                 'description': request.json["description"]}

    entries.append(new_entry)
    return jsonify({"message": "New entry added"})


@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
def edit_one(entry_id):
    """  end point for modifying the entries """

    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    entry[0]['entry_id'] = request.json['entry_id']
    entry[0]['title'] = request.json['title']
    entry[0]['description'] = request.json['description']
    return jsonify(dict(entry=entry[0]))


@app.route('/api/v1/entries/<int:entry_id>', methods=['Delete'])
def delete_one(entry_id):
    """ end point for deleting an item """

    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    entries.remove(entry[0])
    return jsonify({'entries': entries})


@app.errorhandler(404)
def not_found(e):
    return '', 404


if __name__ == '__main__':
    app.run(debug=True)
