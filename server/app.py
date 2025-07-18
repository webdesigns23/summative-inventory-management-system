from flask import Flask, request, jsonify
from server.data import items

app = Flask(__name__)

@app.route("/")
def home():
	return jsonify({"message": "Welcome to the Inventory Management System"})

# GET /inventory → Fetch all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
	return jsonify(items)

# GET /inventory/<id> → Fetch a single item
@app.route("/inventory/<int:id>", methods=["GET"])
def get_inventory_by_id(id):
	pass

# POST /inventory → Add a new item
@app.route("/inventory", methods=["POST"])
def add_inventory_item():
	data = request.get_json()

	if not data or "name" not in data:
		return jsonify({"error": "Missing 'name' in request data"}), 400
	
	new_id = max((item["id"] for item in items), default=0) + 1
	new_item = {"id": new_id, "name": data["name"]}
	items.append(new_item)
	return jsonify(new_item), 201

# PATCH /inventory/<id> → Update an item
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_inventory_item(id):
	pass

# DELETE /inventory/<id> → Remove an item
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_inventory_item(id):
	pass

if __name__ == "__main__":
	app.run(debug=True)