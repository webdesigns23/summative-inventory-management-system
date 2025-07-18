from flask import Flask, request, jsonify
from data import products

app = Flask(__name__)

# GET /inventory → Fetch all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
	return jsonify(products)

# GET /inventory/<id> → Fetch a single item
@app.route("/inventory/<int:id>", methods=["Get"])
def get_inventory_by_id(id):
	pass

# POST /inventory → Add a new item
@app.route("/inventory", methods=["GET"])
def add_item():
	pass

# PATCH /inventory/<id> → Update an item
@app.route("/inventory/<int:id>", methods=["Get"])
def update_item(id):
	pass

# DELETE /inventory/<id> → Remove an item
@app.route("/inventory/<int:id>", methods=["Get"])
def delete_item(id):
	pass