import json
import csv
from datetime import datetime

class Product:
    def __init__(self, name, price, quantity, code):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.code = code

class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0.0

    def add_product(self, product):
        self.inventory[product.code] = product

    def insert_money(self, amount):
        self.balance = round(self.balance + amount, 2)
        return self.balance

    def load_inventory(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.inventory = {}
                for item in data:
                    self.add_product(Product(item['name'], item['price'], item['quantity'], item['code']))
            return True
        except: return False

    def save_inventory(self, filepath):
        data = [{"name": p.name, "price": p.price, "quantity": p.quantity, "code": p.code} for p in self.inventory.values()]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def log_transaction(self, product_name, price):
        log_path = 'data/transactions.csv'
        file_exists = False
        try:
            with open(log_path, 'r'): file_exists = True
        except FileNotFoundError: pass

        with open(log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            # Add header if it's a new file
            if not file_exists:
                writer.writerow(["Timestamp", "Product", "Price"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), product_name, f"${price:.2f}"])

    def restock_all(self, quantity=10):
        for product in self.inventory.values():
            product.quantity = quantity

    def purchase_product(self, code):
        product = self.inventory.get(code)
        if not product or product.quantity <= 0 or self.balance < product.price:
            return False, "Error", 0
        product.quantity -= 1
        price_paid = product.price
        change = round(self.balance - product.price, 2)
        self.balance = 0.0
        return True, f"Dispensed {product.name}. Change: ${change:.2f}", price_paid
