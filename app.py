from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}

user_id_counter = 1

def create_error_response(message, status_code):
    return jsonify({"error": message}), status_code


@app.route('/user', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.json

    if not data or 'name' not in data:
        return create_error_response("Missing 'name' in request body", 400)

    new_user = {
        "id": user_id_counter,
        "name": data['name']
    }

    users[user_id_counter] = new_user
    user_id_counter += 1

    return jsonify(new_user), 201


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return create_error_response("User not found", 404)


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": f"User with id {user_id} deleted"}), 200
    return create_error_response("User not found", 404)