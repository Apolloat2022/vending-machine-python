import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                               QMessageBox)
from PySide6.QtCore import Qt

class VendingMachine:
    def __init__(self):
        self.balance = 0.0
        self.products = {
            "A1": {"name": "Cola", "price": 1.25, "quantity": 10},
            "A2": {"name": "Chips", "price": 1.50, "quantity": 7},
            "A3": {"name": "Water", "price": 1.00, "quantity": 12}
        }
    
    def insert_coin(self, amount):
        self.balance += amount
        return f"Inserted: ${amount:.2f}\nBalance: ${self.balance:.2f}"
    
    def purchase(self, code):
        if code not in self.products:
            return {"success": False, "message": "Invalid code"}
        
        product = self.products[code]
        
        if product["quantity"] <= 0:
            return {"success": False, "message": "Out of stock"}
        
        if self.balance < product["price"]:
            return {"success": False, "message": f"Need: ${product['price']:.2f}"}
        
        product["quantity"] -= 1
        change = self.balance - product["price"]
        self.balance = 0
        
        return {
            "success": True,
            "message": f"Dispensed {product['name']}!\nChange: ${change:.2f}",
            "change": change
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.vm = VendingMachine()
        
        self.setWindowTitle("Vending Machine")
        self.setGeometry(100, 100, 400, 300)
        
        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # Display
        self.display = QLabel("INSERT COINS")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet("background: black; color: lime; font-weight: bold;")
        layout.addWidget(self.display)
        
        # Balance
        self.balance_label = QLabel("Balance: $0.00")
        layout.addWidget(self.balance_label)
        
        # Money buttons
        money_layout = QHBoxLayout()
        for amount in [0.25, 0.50, 1.00]:
            btn = QPushButton(f"${amount:.2f}")
            btn.clicked.connect(lambda checked, a=amount: self.insert_money(a))
            money_layout.addWidget(btn)
        layout.addLayout(money_layout)
        
        # Product buttons
        grid = QGridLayout()
        row, col = 0, 0
        for code, product in self.vm.products.items():
            btn = QPushButton(f"{code}\n{product['name']}\n${product['price']:.2f}")
            btn.clicked.connect(lambda checked, c=code: self.buy_product(c))
            grid.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        layout.addLayout(grid)
    
    def insert_money(self, amount):
        msg = self.vm.insert_coin(amount)
        self.display.setText(msg)
        self.balance_label.setText(f"Balance: ${self.vm.balance:.2f}")
    
    def buy_product(self, code):
        result = self.vm.purchase(code)
        if result["success"]:
            self.display.setText(result["message"])
            QMessageBox.information(self, "Success", result["message"])
        else:
            self.display.setText(result["message"])
            QMessageBox.warning(self, "Failed", result["message"])
        self.balance_label.setText(f"Balance: ${self.vm.balance:.2f}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
