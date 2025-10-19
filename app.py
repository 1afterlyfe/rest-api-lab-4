from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

users = {}
categories = {}
records = {}

user_id_counter = 1
category_id_counter = 1
record_id_counter = 1

def create_error_response(message, status_code):
    return jsonify({"error": message}), status_code

@app.route("/healthcheck")
def healthcheck():
    response_data = {
        "status": "OK",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response_data), 200

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

@app.route('/record', methods=['POST'])
def create_record():
    global record_id_counter
    data = request.json

    required_fields = ['user_id', 'category_id', 'amount']
    if not data or not all(field in data for field in required_fields):
        return create_error_response(f"Missing one of the required fields: {required_fields}", 400)

    user_id = data['user_id']
    category_id = data['category_id']
    amount = data['amount']

    if user_id not in users:
        return create_error_response(f"User with id {user_id} not found", 404)
    if category_id not in categories:
        return create_error_response(f"Category with id {category_id} not found", 404)

    if not isinstance(amount, (int, float)) or amount <= 0:
        return create_error_response("Amount must be a positive number", 400)

    new_record = {
        "id": record_id_counter,
        "user_id": user_id,
        "category_id": category_id,
        "created_at": datetime.datetime.now().isoformat(),
        "amount": amount
    }

    records[record_id_counter] = new_record
    record_id_counter += 1

    return jsonify(new_record), 201


@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = records.get(record_id)
    if record:
        return jsonify(record)
    return create_error_response("Record not found", 404)


@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in records:
        del records[record_id]
        return jsonify({"message": f"Record with id {record_id} deleted"}), 200
    return create_error_response("Record not found", 404)


@app.route('/record', methods=['GET'])
def get_records():
    user_id_arg = request.args.get('user_id')
    category_id_arg = request.args.get('category_id')

    if not user_id_arg and not category_id_arg:
        return create_error_response("At least one filter (user_id or category_id) is required", 400)

    filtered_records = list(records.values())

    if user_id_arg:
        try:
            user_id = int(user_id_arg)
            filtered_records = [r for r in filtered_records if r['user_id'] == user_id]
        except ValueError:
            return create_error_response("Invalid user_id format", 400)

    if category_id_arg:
        try:
            category_id = int(category_id_arg)
            filtered_records = [r for r in filtered_records if r['category_id'] == category_id]
        except ValueError:
            return create_error_response("Invalid category_id format", 400)

    return jsonify(filtered_records)

if __name__ == '__main__':
    app.run(debug=True, port=5000)