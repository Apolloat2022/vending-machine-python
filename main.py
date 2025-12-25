import sys
from PySide6.QtWidgets import QApplication, QPushButton
from src.models import VendingMachine, Product
from src.views import VendingGui

def main():
    app = QApplication(sys.argv)
    vm = VendingMachine()
    products = [
        Product("Cola", 1.50, 5, "A1"), Product("Chips", 1.25, 5, "A2"), Product("Candy", 1.00, 5, "A3"),
        Product("Water", 1.00, 5, "B1"), Product("Juice", 2.00, 5, "B2"), Product("Cookie", 1.50, 5, "B3"),
        Product("Gum", 0.50, 5, "C1"), Product("Coffee", 2.50, 5, "C2"), Product("Tea", 2.00, 5, "C3")
    ]
    for p in products:
        vm.add_product(p)
    window = VendingGui()
    row, col = 0, 0
    for code, prod in vm.inventory.items():
        btn = QPushButton(f"{prod.name}\n${prod.price:.2f}\n({code})")
        btn.setFixedSize(120, 100)
        btn.clicked.connect(lambda chk=False, c=code: attempt_purchase(c))
        window.grid_layout.addWidget(btn, row, col)
        col += 1
        if col > 2:
            col = 0
            row += 1
    def update_display(message):
        window.display.setText(f"BAL: ${vm.balance:.2f}\n{message}")
    def add_money(amount):
        vm.insert_money(amount)
        update_display("MONEY ADDED")
    def attempt_purchase(code):
        success, message = vm.purchase_product(code)
        update_display(message.upper())
    window.btn_dollar.clicked.connect(lambda: add_money(1.00))
    window.btn_quarter.clicked.connect(lambda: add_money(0.25))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
