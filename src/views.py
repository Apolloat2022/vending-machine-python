from PySide6.QtWidgets import (QMainWindow, QWidget, QGridLayout, 
                             QPushButton, QVBoxLayout, QLabel, QHBoxLayout)
from PySide6.QtCore import Qt

class VendingGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Vendor Pro")
        self.setFixedSize(450, 600)
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)
        self.display = QLabel("WELCOME\nINSERT MONEY")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet("background-color: #1a1a1a; color: #00ff00; font-family: 'Courier New'; font-size: 20px; border: 4px solid #333; padding: 10px;")
        self.main_layout.addWidget(self.display)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)
        money_layout = QHBoxLayout()
        self.btn_dollar = QPushButton("Insert $1.00")
        self.btn_quarter = QPushButton("Insert $0.25")
        money_layout.addWidget(self.btn_dollar)
        money_layout.addWidget(self.btn_quarter)
        self.main_layout.addLayout(money_layout)
