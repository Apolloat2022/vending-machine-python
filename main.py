import sys
import os
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Qt
from src.models import VendingMachine, Product
from src.views import VendingGui

def main():
    app = QApplication(sys.argv)
    vm = VendingMachine()
    data_path = os.path.join('data', 'inventory.json')
    
    if not vm.load_inventory(data_path):
        products = [Product("Cola", 1.50, 5, "A1"), Product("Chips", 1.25, 5, "A2"), Product("Candy", 1.00, 5, "A3")]
        for p in products: vm.add_product(p)
        vm.save_inventory(data_path)

    window = VendingGui()
    
    def update_display(message):
        window.display.setText(f"BAL: ${vm.balance:.2f}\n{message}")

    def attempt_purchase(code):
        # We now get back the price_paid to log it
        success, message, price_paid = vm.purchase_product(code)
        if success:
            vm.save_inventory(data_path)
            product_name = vm.inventory[code].name
            vm.log_transaction(product_name, price_paid)
        update_display(message.upper())

    def keyPressEvent(event):
        if event.key() == Qt.Key_R:
            vm.restock_all(10)
            vm.save_inventory(data_path)
            update_display("ADMIN: RESTOCKED")
    window.keyPressEvent = keyPressEvent

    row, col = 0, 0
    for code, prod in vm.inventory.items():
        btn = QPushButton(f"{prod.name}\n${prod.price:.2f}")
        btn.setFixedSize(120, 100)
        btn.clicked.connect(lambda chk=False, c=code: attempt_purchase(c))
        window.grid_layout.addWidget(btn, row, col)
        col += 1
        if col > 2: col = 0; row += 1

    window.btn_dollar.clicked.connect(lambda: (vm.insert_money(1.00), update_display("MONEY ADDED")))
    window.btn_quarter.clicked.connect(lambda: (vm.insert_money(0.25), update_display("MONEY ADDED")))
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
