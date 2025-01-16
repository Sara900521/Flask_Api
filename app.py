from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load users from a JSON file
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

# Save users to a JSON file
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

@app.route('/users', methods=['GET'])
def get_users():
    users = load_users()
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def create_user():
    users = load_users()
    new_user = request.json
    users.append(new_user)
    save_users(users)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        user.update(request.json)
        save_users(users)
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        users.remove(user)
        save_users(users)
        return '', 204
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

