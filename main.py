import sys
import os
from PySide6.QtWidgets import QApplication, QPushButton
from src.models import VendingMachine, Product
from src.views import VendingGui

def main():
    app = QApplication(sys.argv)
    vm = VendingMachine()
    data_path = os.path.join('data', 'inventory.json')
    
    # 24 Premium Items for 2026 Variety
    prods = [
        # --- DRINKS ---
        Product("Coke", 1.75, 10, "A1"), Product("Pepsi", 1.75, 10, "A2"),
        Product("Dr Pepper", 1.75, 10, "A3"), Product("Powerade", 2.25, 10, "B1"),
        Product("Water", 1.25, 10, "B2"), Product("Sparkling", 2.00, 10, "B3"),
        Product("Iced Coffee", 3.50, 10, "C1"), Product("Energy Drk", 3.00, 10, "C2"),
        # --- SNACKS ---
        Product("Classic Chips", 1.50, 10, "C3"), Product("BBQ Chips", 1.50, 10, "D1"),
        Product("Sour Cream", 1.50, 10, "D2"), Product("Pretzels", 1.25, 10, "D3"),
        Product("Mixed Nuts", 2.50, 10, "E1"), Product("Protein Bar", 3.00, 10, "E2"),
        Product("Beef Jerky", 4.50, 10, "E3"), Product("Popcorn", 2.00, 10, "F1"),
        # --- SWEETS ---
        Product("PB Cookie", 2.00, 10, "F2"), Product("Dark Choco", 2.50, 10, "F3"),
        Product("Milk Choco", 2.25, 10, "G1"), Product("Gummy Bears", 1.75, 10, "G2"),
        Product("Skittles", 1.75, 10, "G3"), Product("Brownie", 2.50, 10, "H1"),
        Product("Fruit Snacks", 1.50, 10, "H2"), Product("Mint Gum", 0.75, 10, "H3")
    ]

    # Force update the inventory for the demo
    for p in prods:
        vm.add_product(p)
    vm.save_inventory(data_path)

    window = VendingGui()
    
    def update_ui(msg=""):
        window.display.setText(f"CREDIT: ${vm.balance:.2f}\n{msg}")

    def buy(code):
        success, msg, price = vm.purchase_product(code)
        if success:
            vm.save_inventory(data_path)
            vm.log_transaction(vm.inventory[code].name, price)
        update_ui(msg.upper())

    # Build 3-column grid inside the scroll area
    row, col = 0, 0
    for code, p in vm.inventory.items():
        btn = QPushButton(f"{p.name}\n${p.price:.2f}\n[{code}]")
        btn.setFixedSize(130, 85)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1a2e; color: white; 
                border: 1px solid #FFD700; border-radius: 5px; font-size: 11px;
            }
            QPushButton:hover { background-color: #2a2a4e; border: 1px solid #FFF; }
        """)
        btn.clicked.connect(lambda chk=False, c=code: buy(c))
        window.grid_layout.addWidget(btn, row, col)
        col += 1
        if col > 2: col = 0; row += 1

    window.btn_5.clicked.connect(lambda: (vm.insert_money(5.00), update_ui("ADDED $5.00")))
    window.btn_1.clicked.connect(lambda: (vm.insert_money(1.00), update_ui("ADDED $1.00")))
    window.btn_refund.clicked.connect(lambda: update_ui(f"REFUNDED: ${vm.refund():.2f}"))
    
    update_ui("READY")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
