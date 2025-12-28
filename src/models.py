"""
models.py - Business logic for vending machine
"""

from datetime import datetime
import json
from pathlib import Path


class Product:
    """Represents a single product in the vending machine"""
    
    def __init__(self, code: str, name: str, price: float, quantity: int = 10):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            code=data['code'],
            name=data['name'],
            price=data['price'],
            quantity=data['quantity']
        )
    
    def is_available(self):
        return self.quantity > 0
    
    def can_purchase(self, balance: float):
        return self.is_available() and balance >= self.price
    
    def purchase(self):
        if self.quantity > 0:
            self.quantity -= 1
            return True
        return False


class VendingMachine:
    """Main vending machine business logic"""
    
    def __init__(self):
        self.balance = 0.0
        self.total_sales = 0.0
        self.transactions = []
        self.products = {}
        self.load_default_products()
    
    def load_default_products(self):
        """Load the specific 24 products from the layout"""
        products_data = [
            # Row 1
            ("A1", "Coke", 1.75, 9),
            ("A2", "Pepsi", 1.75, 9),
            ("A3", "Dr Pepper", 1.75, 9),
            ("A4", "Powerade", 2.25, 10),
            # Row 2
            ("B1", "Water", 1.25, 9),
            ("B2", "Sparkling", 2.00, 10),
            ("B3", "Iced Coffee", 3.50, 10),
            ("B4", "Energy Drk", 3.00, 10),
            # Row 3
            ("C1", "Classic Chips", 1.50, 9),
            ("C2", "BBQ Chips", 1.50, 10),
            ("C3", "Sour Cream", 1.50, 10),
            ("C4", "Pretzels", 1.25, 10),
            # Row 4
            ("D1", "Mixed Nuts", 2.50, 10),
            ("D2", "Protein Bar", 3.00, 10),
            ("D3", "Beef Jerky", 4.50, 10),
            ("D4", "Popcorn", 2.00, 10),
            # Row 5
            ("E1", "PB Cookie", 2.00, 10),
            ("E2", "Dark Choco", 2.50, 10),
            ("E3", "Milk Choco", 2.25, 10),
            ("E4", "Gummy Bears", 1.75, 10),
            # Row 6
            ("F1", "Skittles", 1.75, 10),
            ("F2", "Brownie", 2.50, 10),
            ("F3", "Fruit Snacks", 1.50, 10),
            ("F4", "Mint Gum", 0.75, 10),
        ]
        
        for code, name, price, quantity in products_data:
            self.products[code] = Product(code, name, price, quantity)
    
    def insert_cash(self, amount: float):
        if amount <= 0:
            return "Invalid amount"
        
        self.balance += amount
        self.log_transaction(f"Cash inserted: ${amount:.2f}")
        return f"Inserted: ${amount:.2f}"
    
    def process_credit_card(self, amount: float, card_info: dict = None):
        self.balance += amount
        self.log_transaction(f"Credit card payment: ${amount:.2f}")
        return f"Card payment: ${amount:.2f}"
    
    def purchase_product(self, product_code: str):
        result = {
            'success': False,
            'message': '',
            'change': 0.0,
            'product': None
        }
        
        if product_code not in self.products:
            result['message'] = "Invalid product code!"
            return result
        
        product = self.products[product_code]
        
        if not product.is_available():
            result['message'] = f"Sorry, {product.name} is out of stock!"
            return result
        
        if self.balance < product.price:
            result['message'] = f"Insufficient funds! Need: ${product.price:.2f}"
            return result
        
        # Process purchase
        product.purchase()
        change = self.balance - product.price
        self.total_sales += product.price
        self.balance = 0.0
        
        result['success'] = True
        result['message'] = f"Dispensed: {product.name}!"
        result['change'] = change
        result['product'] = product
        
        self.log_transaction(f"Purchased {product.name} for ${product.price:.2f}")
        return result
    
    def cancel_transaction(self):
        change = self.balance
        self.balance = 0.0
        if change > 0:
            self.log_transaction(f"Cancelled. Returned: ${change:.2f}")
        return change
    
    def log_transaction(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"{timestamp}: {message}")
    
    def get_product_grid(self):
        grid = []
        # Sort by row then column
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        cols = ['1', '2', '3', '4']
        
        for row in rows:
            for col in cols:
                code = f"{row}{col}"
                if code in self.products:
                    product = self.products[code]
                    grid.append({
                        'code': code,
                        'name': product.name,
                        'price': product.price,
                        'quantity': product.quantity,
                        'available': product.is_available(),
                        'affordable': product.can_purchase(self.balance)
                    })
        
        return grid
    
    def save_state(self, filename: str = "../data/vending_state.json"):
        Path("../data").mkdir(exist_ok=True)
        state = {
            'products': {code: prod.to_dict() for code, prod in self.products.items()},
            'total_sales': self.total_sales,
            'transactions': self.transactions[-100:]
        }
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filename: str = "../data/vending_state.json"):
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            self.products = {code: Product.from_dict(data) for code, data in state['products'].items()}
            self.total_sales = state['total_sales']
            self.transactions = state.get('transactions', [])
        except FileNotFoundError:
            print("No saved state found. Using defaults.")
        except json.JSONDecodeError:
            print("Error reading saved state. Using defaults.")
