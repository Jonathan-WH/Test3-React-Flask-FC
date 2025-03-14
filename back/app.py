from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

DUMMY_JSON_URL = "https://dummyjson.com/products"

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get("category")  # Récupérer la catégorie
    max_price = request.args.get("max_price", type=float)  # Récupérer le prix max
    sort_by = request.args.get("sort_by")  # Nouveau paramètre pour le tri

    try:
        response = requests.get(DUMMY_JSON_URL)
        response.raise_for_status()
        data = response.json()["products"]  # Récupérer seulement la liste des produits

        # Appliquer les filtres
        if category:
            data = [p for p in data if p["category"].lower() == category.lower()]
        if max_price:
            data = [p for p in data if p["price"] <= max_price]

        # Appliquer le tri
        if sort_by:
            if sort_by == "price_asc":
                data = sorted(data, key=lambda x: x["price"])
            elif sort_by == "price_desc":
                data = sorted(data, key=lambda x: x["price"], reverse=True)
            elif sort_by == "name_asc":
                data = sorted(data, key=lambda x: x["title"].lower())
            elif sort_by == "name_desc":
                data = sorted(data, key=lambda x: x["title"].lower(), reverse=True)

        return jsonify({"products": data})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)