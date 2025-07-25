from flask import Flask, render_template, request, jsonify
import json
import pytesseract
from PIL import Image

app = Flask(__name__)

# Sample inventory data stored in a JSON file
inventory_data = []

# Load data from JSON file
def load_inventory():
    global inventory_data
    try:
        with open('data.json', 'r') as f:
            inventory_data = json.load(f)
    except FileNotFoundError:
        inventory_data = []

# Save data to JSON file
def save_inventory():
    with open('data.json', 'w') as f:
        json.dump(inventory_data, f)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    load_inventory()
    return jsonify(inventory_data)

# Add a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    inventory_data.append(data)
    save_inventory()
    return jsonify({"message": "Item added successfully"}), 201

# Update an item
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    if 0 <= item_id < len(inventory_data):
        inventory_data[item_id] = data
        save_inventory()
        return jsonify({"message": "Item updated successfully"})
    return jsonify({"error": "Item not found"}), 404

# Delete an item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 0 <= item_id < len(inventory_data):
        del inventory_data[item_id]
        save_inventory()
        return jsonify({"message": "Item deleted successfully"})
    return jsonify({"error": "Item not found"}), 404

# Process uploaded image and extract text using OCR
@app.route('/api/extract-text', methods=['POST'])
def extract_text():
    image_file = request.files['image']
    if image_file:
        img = Image.open(image_file.stream)
        extracted_text = pytesseract.image_to_string(img)
        return jsonify({"text": extracted_text})
    return jsonify({"error": "No image provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
