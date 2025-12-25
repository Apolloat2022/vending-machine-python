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

    def purchase_product(self, code):
        product = self.inventory.get(code)
        if not product:
            return False, "Invalid selection."
        if product.quantity <= 0:
            return False, "Out of stock."
        if self.balance < product.price:
            return False, f"Need ${product.price - self.balance:.2f} more."

        product.quantity -= 1
        change = round(self.balance - product.price, 2)
        self.balance = 0.0
        return True, f"Dispensed {product.name}. Change: ${change:.2f}"
