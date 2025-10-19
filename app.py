from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
categories = {}

user_id_counter = 1
category_id_counter = 1

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

@app.route('/category', methods=['POST'])
def create_category():
    global category_id_counter
    data = request.json

    if not data or 'name' not in data:
        return create_error_response("Missing 'name' in request body", 400)

    new_category = {
        "id": category_id_counter,
        "name": data['name']
    }

    categories[category_id_counter] = new_category
    category_id_counter += 1

    return jsonify(new_category), 201

@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values()))

@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = categories.get(category_id)
    if category:
        return jsonify(category)
    return create_error_response("Category not found", 404)

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in categories:
        del categories[category_id]
        return jsonify({"message": f"Category with id {category_id} deleted"}), 200
    return create_error_response("Category not found", 404)