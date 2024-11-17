import os
import json

ORDERS_FILE = os.path.join("data", "orders.json")

def save_order(order):
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

    with open(ORDERS_FILE, "r+", encoding="utf-8") as file:
        orders = json.load(file)
        orders.append(order)
        file.seek(0)
        json.dump(orders, file, indent=4)

def get_pending_order_by_user(user_id):
    if not os.path.exists(ORDERS_FILE):
        return None

    with open(ORDERS_FILE, "r", encoding="utf-8") as file:
        orders = json.load(file)
        for order in orders:
            if order["user_id"] == user_id and order["status"] == "pendiente":
                return order
    return None
