import json
import os

def load_products():
    products_file = os.path.join("data", "products.json")
    if not os.path.exists(products_file):
        raise FileNotFoundError(f"El archivo {products_file} no existe.")
    with open(products_file, "r", encoding="utf-8") as file:
        return json.load(file)

def get_product_by_name(product_name):
    """Busca un producto por su nombre."""
    products = load_products()
    return next((p for p in products if p["name"] == product_name), None)


