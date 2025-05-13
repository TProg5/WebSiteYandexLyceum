from flask import Flask, request, jsonify

app = Flask(__name__)

# тестовые данные в памяти
products = [
    {"id": 1, "name": "Widget", "price": 100},
    {"id": 2, "name": "Gadget", "price": 150},
]

# Получить список
@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(products), 200

# Получить один
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    prod = next((p for p in products if p["id"] == product_id), None)
    return jsonify(prod or {}), (200 if prod else 404)

# Создать
@app.route('/products', methods=['POST'])
def create_product():
    new = request.get_json()
    products.append(new)
    return jsonify(new), 201

# Обновить (полное или частичное)
@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    data = request.get_json()
    for p in products:
        if p["id"] == product_id:
            p.update(data)
            return jsonify(p), 200
    return {}, 404

# Удалить
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return {}, 204

if __name__ == '__main__':
    app.run(debug=True)
