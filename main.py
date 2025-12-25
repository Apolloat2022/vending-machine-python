import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QPushButton
from src.models import VendingMachine, Product
from src.views import VendingGui

def main():
    app = QApplication(sys.argv)
    vm = VendingMachine()
    data_path = os.path.join('data', 'inventory.json')
    
    if not vm.load_inventory(data_path):
        # Default inventory if file doesn't exist
        products = [Product("Cola", 1.50, 5, "A1"), Product("Chips", 1.25, 5, "A2")]
        for p in products: vm.add_product(p)
        vm.save_inventory(data_path)

    window = VendingGui()
    
    # --- NEW YEAR'S LOGIC ---
    now = datetime.now()
    is_new_year = (now.month == 1 and now.day == 1)
    
    if is_new_year:
        window.apply_new_years_theme()
        for prod in vm.inventory.values():
            prod.price = round(prod.price * 0.8, 2) # 20% Discount
    # ------------------------

    def update_display(message):
        prefix = "✨ " if is_new_year else "BAL: "
        window.display.setText(f"{prefix}${vm.balance:.2f}\n{message}")

    def attempt_purchase(code):
        success, message = vm.purchase_product(code)
        if success:
            vm.save_inventory(data_path)
        update_display(message.upper())

    # Create buttons
    row, col = 0, 0
    for code, prod in vm.inventory.items():
        label = f"{prod.name}\n${prod.price:.2f}"
        if is_new_year: label = "🎊 " + label
        btn = QPushButton(label)
        btn.setFixedSize(120, 100)
        btn.clicked.connect(lambda chk=False, c=code: attempt_purchase(c))
        window.grid_layout.addWidget(btn, row, col)
        col += 1
        if col > 2: col = 0; row += 1

    window.btn_dollar.clicked.connect(lambda: (vm.insert_money(1.00), update_display("MONEY ADDED")))
    window.btn_quarter.clicked.connect(lambda: (vm.insert_money(0.25), update_display("MONEY ADDED")))
    
    update_display("HAPPY NEW YEAR!" if is_new_year else "WELCOME")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
