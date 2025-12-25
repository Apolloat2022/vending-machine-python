from PySide6.QtWidgets import (QMainWindow, QWidget, QGridLayout, 
                             QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea)
from PySide6.QtCore import Qt

class VendingGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Global Vendor 2026")
        # Reduced height to ensure it fits on laptop screens
        self.setFixedSize(480, 650) 
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setStyleSheet("background-color: #050510;")
        self.main_layout = QVBoxLayout(self.central)
        
        # Compact Digital Display
        self.display = QLabel("WELCOME 2026")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet("""
            background-color: #000; color: #FFD700; 
            font-family: 'Segoe UI'; font-weight: bold; font-size: 20px; 
            border: 2px solid #FFD700; border-radius: 8px;
            padding: 10px; margin: 5px;
        """)
        self.main_layout.addWidget(self.display)
        
        # Scroll Area for Products
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background-color: transparent;")
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.scroll.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll)
        
        # Control Panel
        money_layout = QHBoxLayout()
        self.btn_5 = QPushButton("Insert $5")
        self.btn_1 = QPushButton("Insert $1")
        self.btn_refund = QPushButton("Refund")
        
        for btn in [self.btn_5, self.btn_1, self.btn_refund]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFD700; color: #000; font-weight: bold;
                    border-radius: 5px; height: 35px;
                }
                QPushButton:hover { background-color: #FFF; }
            """)
        money_layout.addWidget(self.btn_5)
        money_layout.addWidget(self.btn_1)
        money_layout.addWidget(self.btn_refund)
        self.main_layout.addLayout(money_layout)
