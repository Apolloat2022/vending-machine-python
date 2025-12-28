"""
views.py - Cinematic modern vending machine UI
"""

import sys
import os
import random
from datetime import datetime

# Fix import path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QMessageBox, QDialog,
    QLineEdit, QGroupBox, QFormLayout, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient

# Try to import our styles
try:
    # We'll define styles inline if import fails
    pass
except ImportError:
    pass

# Import business logic
try:
    from models import VendingMachine
    print("✓ Models imported successfully")
except ImportError:
    print("Models import failed, creating fallback")
    # Create simple fallback
    from datetime import datetime
    import json
    from pathlib import Path
    
    class Product:
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
        def __init__(self):
            self.balance = 0.0
            self.total_sales = 0.0
            self.transactions = []
            self.products = {}
            self.load_default_products()
        
        def load_default_products(self):
            products_data = [
                ("A1", "Coke", 1.75, 9),
                ("A2", "Pepsi", 1.75, 9),
                ("A3", "Dr Pepper", 1.75, 9),
                ("A4", "Powerade", 2.25, 10),
                ("B1", "Water", 1.25, 9),
                ("B2", "Sparkling", 2.00, 10),
                ("B3", "Iced Coffee", 3.50, 10),
                ("B4", "Energy Drk", 3.00, 10),
                ("C1", "Classic Chips", 1.50, 9),
                ("C2", "BBQ Chips", 1.50, 10),
                ("C3", "Sour Cream", 1.50, 10),
                ("C4", "Pretzels", 1.25, 10),
                ("D1", "Mixed Nuts", 2.50, 10),
                ("D2", "Protein Bar", 3.00, 10),
                ("D3", "Beef Jerky", 4.50, 10),
                ("D4", "Popcorn", 2.00, 10),
                ("E1", "PB Cookie", 2.00, 10),
                ("E2", "Dark Choco", 2.50, 10),
                ("E3", "Milk Choco", 2.25, 10),
                ("E4", "Gummy Bears", 1.75, 10),
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
        
        def save_state(self, filename: str = "data/vending_state.json"):
            Path("data").mkdir(exist_ok=True)
            state = {
                'products': {code: prod.to_dict() for code, prod in self.products.items()},
                'total_sales': self.total_sales,
                'transactions': self.transactions[-100:]
            }
            with open(filename, 'w') as f:
                json.dump(state, f, indent=2)
        
        def load_state(self, filename: str = "data/vending_state.json"):
            try:
                with open(filename, 'r') as f:
                    state = json.load(f)
                self.products = {code: Product(code=data['name'], **data) for code, data in state['products'].items()}
                self.total_sales = state['total_sales']
                self.transactions = state.get('transactions', [])
            except FileNotFoundError:
                print("No saved state found. Using defaults.")
            except json.JSONDecodeError:
                print("Error reading saved state. Using defaults.")


# ========== CINEMATIC STYLES ==========
CINEMATIC_STYLESHEET = """
/* Main Application */
QMainWindow {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                stop:0 #0a0a1a, stop:1 #1a1a2e);
    color: #ffffff;
    font-family: 'Segoe UI', 'Arial', sans-serif;
}

/* Buttons - Modern Glass Effect */
QPushButton {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.15),
                                stop:1 rgba(255, 255, 255, 0.05));
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: white;
    font-weight: 600;
    padding: 12px 20px;
    font-size: 14px;
    min-height: 40px;
}

QPushButton:hover {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.25),
                                stop:1 rgba(255, 255, 255, 0.15));
    border: 2px solid rgba(0, 255, 136, 0.7);
    color: #00ff88;
}

QPushButton:pressed {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 255, 136, 0.4),
                                stop:1 rgba(0, 255, 136, 0.2));
    border: 2px solid #00ff88;
}

/* Labels */
QLabel {
    color: #ffffff;
    background: transparent;
}

/* Group Boxes */
QGroupBox {
    background: rgba(30, 30, 46, 0.8);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    margin-top: 10px;
    padding-top: 15px;
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 15px;
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00ff88, stop:1 #0088ff);
    color: #000000;
    border-radius: 8px;
    font-weight: bold;
}

/* Line Edits */
QLineEdit {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    color: white;
    selection-background-color: #00ff88;
}

QLineEdit:focus {
    border: 2px solid #00ff88;
    background: rgba(255, 255, 255, 0.15);
}
"""


class ModernProductButton(QPushButton):
    """Cinematic product button"""
    
    clicked_with_code = Signal(str)
    
    def __init__(self, product_info: dict):
        super().__init__()
        self.product_code = product_info['code']
        self.product_info = product_info
        
        self.setup_button()
        self.clicked.connect(self.on_click)
    
    def setup_button(self):
        """Setup button appearance"""
        emoji = self.get_product_emoji(self.product_info['name'])
        text = f"{emoji} {self.product_info['name']}\n${self.product_info['price']:.2f}\n{self.product_info['quantity']} units"
        self.setText(text)
        
        self.setMinimumSize(140, 100)
        self.setMaximumSize(160, 120)
        
        if self.product_info['available'] and self.product_info['affordable']:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                                stop:0 rgba(0, 255, 136, 0.3),
                                                stop:1 rgba(0, 136, 255, 0.3));
                    border: 2px solid #00ff88;
                    border-radius: 12px;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    font-size: 11px;
                    text-align: center;
                }
                QPushButton:hover {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                                stop:0 rgba(0, 255, 136, 0.5),
                                                stop:1 rgba(0, 136, 255, 0.5));
                    border: 2px solid #00ff88;
                }
            """)
            self.setEnabled(True)
        elif not self.product_info['available']:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.05);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    color: #888888;
                    font-weight: bold;
                    padding: 8px;
                    font-size: 11px;
                    text-align: center;
                }
            """)
            self.setEnabled(False)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                                stop:0 rgba(0, 136, 255, 0.3),
                                                stop:1 rgba(136, 0, 255, 0.3));
                    border: 2px solid #0088ff;
                    border-radius: 12px;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    font-size: 11px;
                    text-align: center;
                }
            """)
            self.setEnabled(False)
    
    def get_product_emoji(self, name: str) -> str:
        """Get emoji for product"""
        emoji_map = {
            'cola': '🥤', 'coke': '🥤', 'pepsi': '🥤',
            'water': '💧', 'sparkling': '💦',
            'coffee': '☕', 'energy': '⚡',
            'chips': '🥔', 'pretzels': '🥨',
            'nuts': '🥜', 'protein': '💪',
            'jerky': '🥩', 'popcorn': '🍿',
            'cookie': '🍪', 'choco': '🍫',
            'gummy': '🍬', 'skittles': '🌈',
            'brownie': '🍰', 'fruit': '🍎',
            'gum': '🍬'
        }
        
        name_lower = name.lower()
        for key, emoji in emoji_map.items():
            if key in name_lower:
                return emoji
        return '📦'
    
    def on_click(self):
        self.clicked_with_code.emit(self.product_code)
    
    def update_info(self, product_info: dict):
        """Update button with new info"""
        self.product_info = product_info
        emoji = self.get_product_emoji(product_info['name'])
        text = f"{emoji} {product_info['name']}\n${product_info['price']:.2f}\n{product_info['quantity']} units"
        self.setText(text)
        
        if product_info['available'] and product_info['affordable']:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                                stop:0 rgba(0, 255, 136, 0.3),
                                                stop:1 rgba(0, 136, 255, 0.3));
                    border: 2px solid #00ff88;
                    border-radius: 12px;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    font-size: 11px;
                    text-align: center;
                }
                QPushButton:hover {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                                stop:0 rgba(0, 255, 136, 0.5),
                                                stop:1 rgba(0, 136, 255, 0.5));
                    border: 2px solid #00ff88;
                }
            """)
            self.setEnabled(True)
        elif not product_info['available']:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.05);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    color: #888888;
                    font-weight: bold;
                    padding: 8px;
                    font-size: 11px;
                    text-align: center;
                }
            """)
            self.setEnabled(False)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                                stop:0 rgba(0, 136, 255, 0.3),
                                                stop:1 rgba(136, 0, 255, 0.3));
                    border: 2px solid #0088ff;
                    border-radius: 12px;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    font-size: 11px;
                    text-align: center;
                }
            """)
            self.setEnabled(False)


class CreditCardDialog(QDialog):
    """Modern credit card payment dialog"""
    
    payment_complete = Signal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("💳 Cinematic Payment")
        self.setModal(True)
        self.resize(450, 350)
        self.setStyleSheet(CINEMATIC_STYLESHEET)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header
        header = QLabel("⚡ CINEMATIC PAYMENT ⚡")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #00ff88, stop:0.5 #0088ff, stop:1 #ff0088);
                color: #000000;
                padding: 12px;
                border-radius: 10px;
            }
        """)
        layout.addWidget(header)
        
        # Form
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        
        # Card number
        card_layout = QHBoxLayout()
        card_layout.addWidget(QLabel("💳 Card Number:"))
        self.card_number = QLineEdit()
        self.card_number.setPlaceholderText("1234 5678 9012 3456")
        self.card_number.setMaxLength(19)
        card_layout.addWidget(self.card_number)
        form_layout.addLayout(card_layout)
        
        # Expiry and CVV
        details_layout = QHBoxLayout()
        
        expiry_layout = QVBoxLayout()
        expiry_layout.addWidget(QLabel("📅 Expiry (MM/YY):"))
        self.expiry_date = QLineEdit()
        self.expiry_date.setPlaceholderText("12/25")
        self.expiry_date.setMaxLength(5)
        expiry_layout.addWidget(self.expiry_date)
        
        cvv_layout = QVBoxLayout()
        cvv_layout.addWidget(QLabel("🔒 CVV:"))
        self.cvv = QLineEdit()
        self.cvv.setPlaceholderText("123")
        self.cvv.setMaxLength(4)
        self.cvv.setEchoMode(QLineEdit.Password)
        cvv_layout.addWidget(self.cvv)
        
        details_layout.addLayout(expiry_layout)
        details_layout.addLayout(cvv_layout)
        form_layout.addLayout(details_layout)
        
        # Amount
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("💰 Amount ($):"))
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("10.00")
        amount_layout.addWidget(self.amount)
        form_layout.addLayout(amount_layout)
        
        layout.addWidget(form_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        pay_button = QPushButton("⚡ Process Payment")
        pay_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(147, 51, 234, 0.8),
                                            stop:1 rgba(79, 70, 229, 0.8));
                border: 2px solid rgba(147, 51, 234, 0.5);
                color: white;
                font-weight: bold;
                padding: 12px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(167, 71, 254, 0.9),
                                            stop:1 rgba(99, 90, 249, 0.9));
                border: 2px solid #9333ea;
            }
        """)
        pay_button.clicked.connect(self.process_payment)
        
        cancel_button = QPushButton("❌ Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.8);
                border: 2px solid rgba(239, 68, 68, 0.5);
                color: white;
                padding: 12px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: rgba(248, 113, 113, 0.9);
                border: 2px solid #ef4444;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(pay_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def process_payment(self):
        try:
            amount = float(self.amount.text())
            if amount <= 0:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a positive amount")
                return
            
            card_num = self.card_number.text().replace(" ", "")
            if len(card_num) < 16:
                QMessageBox.warning(self, "Invalid Card", "Please enter a valid 16-digit card number")
                return
            
            QMessageBox.information(self, "Processing", "⚡ Processing payment... Please wait.")
            QTimer.singleShot(1500, lambda: self.finalize_payment(amount))
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Amount", "Please enter a valid amount")
    
    def finalize_payment(self, amount: float):
        self.payment_complete.emit(amount)
        self.accept()
        QMessageBox.information(self, "Success", f"✅ Payment of ${amount:.2f} processed successfully!")


class CinematicMainWindow(QMainWindow):
    """Cinematic main window"""
    
    def __init__(self):
        super().__init__()
        self.vending_machine = VendingMachine()
        self.product_buttons = {}
        
        self.setWindowTitle("Vendor Pro 2026 - Cinematic Edition")
        self.setGeometry(50, 50, 1400, 800)
        self.setStyleSheet(CINEMATIC_STYLESHEET)
        
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(main_layout)
        
        # ========== LEFT CONTROL PANEL ==========
        left_panel = QFrame()
        left_panel.setMaximumWidth(350)
        left_panel.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 46, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 15px;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        
        # Cinematic Header
        header = QLabel("🎬 VENDOR PRO 2026 🎬")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #00ff88, stop:0.3 #0088ff, 
                                            stop:0.6 #ff0088, stop:1 #ffaa00);
                color: #000000;
                padding: 20px;
                border-radius: 15px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
        """)
        left_layout.addWidget(header)
        
        # Credit Display
        credit_frame = QFrame()
        credit_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(30, 64, 175, 0.9),
                                            stop:1 rgba(29, 78, 216, 0.9));
                border: 3px solid rgba(59, 130, 246, 0.5);
                border-radius: 15px;
            }
        """)
        credit_layout = QVBoxLayout(credit_frame)
        
        credit_label = QLabel("💰 AVAILABLE CREDIT")
        credit_label.setAlignment(Qt.AlignCenter)
        credit_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; padding: 5px;")
        
        self.credit_display = QLabel("$0.00")
        self.credit_display.setAlignment(Qt.AlignCenter)
        self.credit_display.setStyleSheet("""
            QLabel {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 52px;
                font-weight: bold;
                color: white;
                padding: 20px;
            }
        """)
        
        credit_layout.addWidget(credit_label)
        credit_layout.addWidget(self.credit_display)
        left_layout.addWidget(credit_frame)
        
        # Money Buttons
        money_group = QGroupBox("💸 ADD MONEY")
        money_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #00ff88;
            }
        """)
        money_layout = QGridLayout()
        money_layout.setSpacing(10)
        
        money_buttons = [
            ("➕ $5", 5.00, "#4CAF50"),
            ("➕ $1", 1.00, "#2196F3"),
            ("➕ $0.25", 0.25, "#FF9800"),
            ("➕ $0.10", 0.10, "#9C27B0"),
            ("➕ $0.05", 0.05, "#795548"),
            ("➕ $20", 20.00, "#F44336"),
        ]
        
        for i, (text, value, color) in enumerate(money_buttons):
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qradialgradient(cx:0.3, cy:0.3, radius:1,
                                                fx:0.3, fy:0.3,
                                                stop:0 {color},
                                                stop:1 {self.darken_color(color)});
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 50px;
                    color: white;
                    font-weight: bold;
                    padding: 15px;
                    font-size: 14px;
                    min-width: 90px;
                    min-height: 70px;
                }}
                QPushButton:hover {{
                    border: 2px solid #00ff88;
                    transform: scale(1.05);
                }}
            """)
            btn.clicked.connect(lambda checked, v=value: self.add_money(v))
            money_layout.addWidget(btn, i // 2, i % 2)
        
        money_group.setLayout(money_layout)
        left_layout.addWidget(money_group)
        
        # Action Buttons
        card_btn = QPushButton("💳 CINEMATIC CARD PAYMENT")
        card_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(147, 51, 234, 0.9),
                                            stop:1 rgba(79, 70, 229, 0.9));
                border: 2px solid rgba(147, 51, 234, 0.5);
                border-radius: 12px;
                color: white;
                font-weight: bold;
                padding: 18px;
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(167, 71, 254, 1.0),
                                            stop:1 rgba(99, 90, 249, 1.0));
                border: 2px solid #9333ea;
                box-shadow: 0 0 20px rgba(147, 51, 234, 0.7);
            }
        """)
        card_btn.clicked.connect(self.show_credit_card)
        
        eject_btn = QPushButton("🔄 EJECT CHANGE")
        eject_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(239, 68, 68, 0.9),
                                            stop:1 rgba(220, 38, 38, 0.9));
                border: 2px solid rgba(239, 68, 68, 0.5);
                border-radius: 12px;
                color: white;
                font-weight: bold;
                padding: 18px;
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(248, 113, 113, 1.0),
                                            stop:1 rgba(239, 68, 68, 1.0));
                border: 2px solid #ef4444;
                box-shadow: 0 0 20px rgba(239, 68, 68, 0.7);
            }
        """)
        eject_btn.clicked.connect(self.eject_change)
        
        admin_btn = QPushButton("⚙️ CINEMATIC ADMIN")
        admin_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(96, 125, 139, 0.9),
                                            stop:1 rgba(69, 90, 100, 0.9));
                border: 2px solid rgba(96, 125, 139, 0.5);
                border-radius: 12px;
                color: white;
                font-weight: bold;
                padding: 15px;
                font-size: 14px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                            stop:0 rgba(120, 144, 156, 1.0),
                                            stop:1 rgba(84, 110, 122, 1.0));
                border: 2px solid #607d8b;
            }
        """)
        admin_btn.clicked.connect(self.show_admin)
        
        left_layout.addWidget(card_btn)
        left_layout.addWidget(eject_btn)
        left_layout.addWidget(admin_btn)
        left_layout.addStretch()
        
        main_layout.addWidget(left_panel)
        
        # ========== RIGHT PRODUCT GRID ==========
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 35, 0.8);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        
        # Grid Header
        grid_header = QLabel("🎯 PRODUCT SELECTION 🎯")
        grid_header.setAlignment(Qt.AlignCenter)
        grid_header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                background: rgba(0, 255, 136, 0.2);
                color: #00ff88;
                padding: 15px;
                border-radius: 10px;
                border-bottom: 3px solid #00ff88;
                margin-bottom: 15px;
            }
        """)
        right_layout.addWidget(grid_header)
        
        # Product Grid
        self.product_grid = QGridLayout()
        self.product_grid.setSpacing(15)
        self.product_grid.setContentsMargins(10, 10, 10, 10)
        
        self.load_product_grid()
        
        grid_widget = QWidget()
        grid_widget.setLayout(self.product_grid)
        right_layout.addWidget(grid_widget)
        
        main_layout.addWidget(right_panel, 1)
        
        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: rgba(0, 0, 0, 0.9);
                color: #00ff88;
                font-weight: bold;
                border-top: 2px solid rgba(0, 255, 136, 0.3);
                padding: 5px;
            }
        """)
        self.status_bar.showMessage("🎬 Ready for cinematic vending experience!")
    
    def darken_color(self, hex_color: str) -> str:
        """Darken hex color"""
        color_map = {
            "#4CAF50": "#388E3C",
            "#2196F3": "#1976D2",
            "#FF9800": "#F57C00",
            "#9C27B0": "#7B1FA2",
            "#795548": "#5D4037",
            "#F44336": "#D32F2F",
        }
        return color_map.get(hex_color, hex_color)
    
    def load_product_grid(self):
        """Load products into grid"""
        for i in reversed(range(self.product_grid.count())):
            widget = self.product_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        products = self.vending_machine.get_product_grid()
        positions = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 0), (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 1), (3, 2), (3, 3),
            (4, 0), (4, 1), (4, 2), (4, 3),
            (5, 0), (5, 1), (5, 2), (5, 3)
        ]
        
        for i, (row, col) in enumerate(positions):
            if i < len(products):
                product_info = products[i]
                button = ModernProductButton(product_info)
                button.clicked_with_code.connect(self.purchase_product)
                self.product_grid.addWidget(button, row, col)
                self.product_buttons[product_info['code']] = button
    
    def add_money(self, amount: float):
        """Add money with animation"""
        self.vending_machine.insert_cash(amount)
        self.update_display()
        self.status_bar.showMessage(f"💰 Added ${amount:.2f} - Ready to purchase!")
        
        # Animation effect
        self.animate_credit_display()
    
    def animate_credit_display(self):
        """Animate credit display"""
        animation = QPropertyAnimation(self.credit_display, b"styleSheet")
        animation.setDuration(300)
        original_style = self.credit_display.styleSheet()
        animation.setStartValue(original_style)
        animation.setKeyValueAt(0.5, original_style + "color: #ffd700;")
        animation.setEndValue(original_style)
        animation.start()
    
    def show_credit_card(self):
        """Show credit card dialog"""
        dialog = CreditCardDialog(self)
        dialog.payment_complete.connect(self.process_credit_card)
        dialog.exec()
    
    def process_credit_card(self, amount: float):
        """Process credit card payment"""
        self.vending_machine.process_credit_card(amount)
        self.update_display()
        self.status_bar.showMessage(f"💳 Card payment: ${amount:.2f} added!")
        QMessageBox.information(self, "Payment Success", 
            f"✅ ${amount:.2f} added to balance!\n\nReady for cinematic shopping!")
    
    def purchase_product(self, product_code: str):
        """Purchase product with cinematic effects"""
        result = self.vending_machine.purchase_product(product_code)
        
        if result['success']:
            self.status_bar.showMessage(f"🎉 Enjoy your {result['product'].name}!")
            QMessageBox.information(self, "Cinematic Success!", 
                f"✨ {result['product'].name} DISPENSED! ✨\n\n"
                f"💵 Change: ${result['change']:.2f}\n"
                f"🍿 Enjoy your snack!\n\n"
                f"Thank you for shopping with Vendor Pro 2026! 🎬")
            
            # Animate the purchased button
            if product_code in self.product_buttons:
                button = self.product_buttons[product_code]
                self.animate_purchase(button)
        else:
            self.status_bar.showMessage(result['message'])
            QMessageBox.warning(self, "Cannot Purchase", 
                f"⚠️ {result['message']}\n\n"
                f"Please add more credit or select another item.")
        
        self.update_display()
        self.vending_machine.save_state()
    
    def animate_purchase(self, button):
        """Animate button after purchase"""
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(500)
        start_geo = button.geometry()
        animation.setStartValue(start_geo)
        animation.setKeyValueAt(0.3, start_geo.adjusted(-10, -10, 10, 10))
        animation.setEndValue(start_geo)
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.start()
    
    def eject_change(self):
        """Eject change with cinematic effect"""
        change = self.vending_machine.cancel_transaction()
        if change > 0:
            self.status_bar.showMessage(f"💸 Change ejected: ${change:.2f}")
            QMessageBox.information(self, "Change Ejected", 
                f"💰 ${change:.2f} RETURNED!\n\n"
                f"Coins dispensing now...\n"
                f"Thank you for using Vendor Pro 2026! 🎬")
        else:
            self.status_bar.showMessage("No money to return")
            QMessageBox.information(self, "No Change", 
                "No money to return.\n\nAdd credit to make a purchase! 💰")
        
        self.update_display()
    
    def show_admin(self):
        """Show admin panel"""
        QMessageBox.information(self, "🎬 Cinematic Admin Panel", 
            f"ADMIN FEATURES:\n\n"
            f"💰 Total Sales: ${self.vending_machine.total_sales:.2f}\n"
            f"📦 Total Products: {len(self.vending_machine.products)}\n"
            f"🔄 Restock All Products\n"
            f"📊 View Transaction Logs\n"
            f"⚙️ Configure Machine Settings\n\n"
            f"Password: cinematic2026")
    
    def update_display(self):
        """Update all displays"""
        # Update credit
        self.credit_display.setText(f"${self.vending_machine.balance:.2f}")
        
        # Update product buttons
        products = self.vending_machine.get_product_grid()
        for product_info in products:
            if product_info['code'] in self.product_buttons:
                button = self.product_buttons[product_info['code']]
                button.update_info(product_info)
    
    def closeEvent(self, event):
        """Save state when closing"""
        self.vending_machine.save_state()
        QMessageBox.information(self, "Goodbye!", 
            "Thank you for using Vendor Pro 2026!\n\n"
            "Your session has been saved. 🎬")
        event.accept()
