from flask import Flask, request, jsonify
from inventory import items
import inventory as inventory
import requests

app = Flask(__name__)

@app.route("/")
def home():
	return jsonify({"message": "Welcome to the Inventory Management System"})

# GET /inventory Fetch all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
	return jsonify(items)

# GET /inventory/<id> Fetch a single item
@app.route("/inventory/<int:id>", methods=["GET"])
def get_inventory_by_id(id):
	item = next((item for item in items if item['id'] == id), None)
	if item:
		return jsonify(item)
	return jsonify ({"error":"Item not found"}), 404

# POST /inventory Add a new item
@app.route("/inventory", methods=["POST"])
def add_inventory_item():
	data = request.get_json()
	if not data or "name" not in data:
		return jsonify({"error": "Missing 'name' in request data"}), 400
	
	new_id = max((item["id"] for item in items), default=0) + 1
	new_item = {"id": new_id, "name": data["name"], "barcode": data["barcode"], "price": data["price"], "stock": data["stock"]}
	items.append(new_item)
	return jsonify(new_item), 201

# PATCH /inventory/<id> Update an item
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_inventory_item(id):
	data = request.get_json()
	item = next((item for item in items if item['id'] == id), None)
	if not item:
		return jsonify({"error":"Item not found"}), 404
	
	if "price" in data:
		item["price"] = data["price"]
	if "stock" in data:
		item["stock"] = data["stock"]
	return jsonify(item)

# DELETE /inventory/<id> Remove an item
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_inventory_item(id):
	global items
	item = next((item for item in items if item['id'] == id), None)
	if not item:
		return jsonify({"message":"Item not found"}), 404
	items = [item for item in items if item['id'] != id]
	return jsonify({"message":"Item deleted"}), 200 or 204

# GET Count Helper
@app.route("/inventory/count", methods=["GET"])
def count_items():
	count = len(inventory.items)
	return jsonify({"count": count}), 200

# GET /inventory/<id>/enchance Lfrom External API.
@app.route("/inventory/<int:id>/enhance", methods=["GET"])
def enhance_inventory_item(id):
	item = next((item for item in items if item['id'] == id), None)
	if not item:
		return jsonify({"message":"Item not found"}), 404
	
	try:
		barcode = item.get("barcode")
		if not barcode:
			return jsonify({"error": "Barcode not found"}), 400
		response = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json")
		
		if response.status_code != 200:
			return jsonify({"error": "Failed to fetch data"})
		
		product_data = response.json().get("product", {})

		item["brand"] = product_data.get("brands_owner", "")
		item["ingredients"] = product_data.get("ingredients_text", "")
		item["allergens"] = product_data.get("allergens_hierarchy", [])

		return jsonify(item), 200
	except Exception as error:
		return jsonify({"error": error}), 500


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*' 
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type' 
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE'
    return response

if __name__ == "__main__":
	app.run(debug=True)