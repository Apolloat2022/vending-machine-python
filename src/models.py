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
        with open(log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), product_name, f"${price:.2f}"])

    def purchase_product(self, code):
        product = self.inventory.get(code)
        if not product: return False, "Invalid Code", 0
        if product.quantity <= 0: return False, "Out of Stock", 0
        if self.balance < product.price: return False, "Insufficient Funds", 0
        
        product.quantity -= 1
        self.balance = round(self.balance - product.price, 2) # KEEP THE REMAINING BALANCE
        return True, f"Enjoy your {product.name}!", product.price

    def refund(self):
        amount = self.balance
        self.balance = 0.0
        return amount
