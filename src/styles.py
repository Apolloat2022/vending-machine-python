"""
styles.py - Cinematic modern styles for vending machine
"""

# ========== CINEMATIC DARK THEME ==========
CINEMATIC_STYLESHEET = """
/* Main Application */
QMainWindow {
    background-color: #0a0a0f;
    border: 1px solid #2a2a3a;
}

/* Generic Widgets */
QWidget {
    color: #ffffff;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    selection-background-color: #00ff88;
}

/* Labels */
QLabel {
    background: transparent;
    color: #ffffff;
}

/* Push Buttons - Modern Glass Effect */
QPushButton {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.1),
                                stop:1 rgba(255, 255, 255, 0.05));
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: white;
    font-weight: 600;
    padding: 12px 20px;
    font-size: 14px;
    min-height: 40px;
}

QPushButton:hover {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.15),
                                stop:1 rgba(255, 255, 255, 0.1));
    border: 1px solid rgba(0, 255, 136, 0.5);
    color: #00ff88;
}

QPushButton:pressed {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 255, 136, 0.3),
                                stop:1 rgba(0, 255, 136, 0.1));
    border: 1px solid #00ff88;
}

QPushButton:disabled {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #666666;
}

/* Group Boxes - Glass Panels */
QGroupBox {
    background: rgba(20, 20, 30, 0.7);
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
    border: 1px solid rgba(255, 255, 255, 0.3);
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

/* Dialog Windows */
QDialog {
    background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                                fx:0.5, fy:0.5,
                                stop:0 rgba(10, 10, 20, 0.95),
                                stop:1 rgba(5, 5, 15, 0.95));
    border: 2px solid #00ff88;
    border-radius: 20px;
}

/* Scroll Bars */
QScrollBar:vertical {
    border: none;
    background: rgba(255, 255, 255, 0.05);
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00ff88, stop:1 #0088ff);
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00ffaa, stop:1 #00aaff);
}

/* Status Bar */
QStatusBar {
    background: rgba(0, 0, 0, 0.8);
    color: #00ff88;
    font-weight: bold;
    border-top: 1px solid rgba(0, 255, 136, 0.3);
}

/* Table Widgets */
QTableWidget {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    gridline-color: rgba(255, 255, 255, 0.1);
}

QHeaderView::section {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 255, 136, 0.3),
                                stop:1 rgba(0, 136, 255, 0.3));
    color: white;
    padding: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-weight: bold;
}

/* Progress Bar */
QProgressBar {
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}

QProgressBar::chunk {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00ff88, stop:1 #0088ff);
    border-radius: 8px;
}
"""

# ========== SPECIALIZED STYLES ==========
PRODUCT_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.15),
                                stop:1 rgba(255, 255, 255, 0.05));
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    color: #ffffff;
    font-weight: 600;
    padding: 8px;
    font-size: 12px;
    text-align: center;
}

QPushButton:hover {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 255, 136, 0.3),
                                stop:1 rgba(0, 136, 255, 0.3));
    border: 2px solid #00ff88;
    transform: scale(1.02);
}

QPushButton:pressed {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 255, 136, 0.5),
                                stop:1 rgba(0, 136, 255, 0.5));
}

QPushButton:disabled {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    color: #888888;
}
"""

MONEY_BUTTON_STYLE = """
QPushButton {
    background: qradialgradient(cx:0.3, cy:0.3, radius:1,
                                fx:0.3, fy:0.3,
                                stop:0 rgba(255, 215, 0, 0.8),
                                stop:1 rgba(218, 165, 32, 0.8));
    border: 2px solid rgba(255, 215, 0, 0.5);
    border-radius: 50px;
    color: #000000;
    font-weight: bold;
    padding: 15px;
    font-size: 14px;
    min-width: 80px;
    min-height: 60px;
}

QPushButton:hover {
    background: qradialgradient(cx:0.3, cy:0.3, radius:1,
                                fx:0.3, fy:0.3,
                                stop:0 rgba(255, 223, 0, 0.9),
                                stop:1 rgba(255, 193, 7, 0.9));
    border: 2px solid #ffd700;
    transform: scale(1.05);
}

QPushButton:pressed {
    background: qradialgradient(cx:0.3, cy:0.3, radius:1,
                                fx:0.3, fy:0.3,
                                stop:0 rgba(255, 193, 7, 0.9),
                                stop:1 rgba(255, 160, 0, 0.9));
}
"""

CREDIT_CARD_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(147, 51, 234, 0.8),
                                stop:1 rgba(79, 70, 229, 0.8));
    border: 2px solid rgba(147, 51, 234, 0.5);
    border-radius: 12px;
    color: white;
    font-weight: bold;
    padding: 18px;
    font-size: 16px;
}

QPushButton:hover {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(167, 71, 254, 0.9),
                                stop:1 rgba(99, 90, 249, 0.9));
    border: 2px solid #9333ea;
    box-shadow: 0 0 15px rgba(147, 51, 234, 0.5);
}

QPushButton:pressed {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(127, 31, 214, 0.9),
                                stop:1 rgba(69, 60, 209, 0.9));
}
"""

EJECT_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(239, 68, 68, 0.8),
                                stop:1 rgba(220, 38, 38, 0.8));
    border: 2px solid rgba(239, 68, 68, 0.5);
    border-radius: 12px;
    color: white;
    font-weight: bold;
    padding: 18px;
    font-size: 16px;
}

QPushButton:hover {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(248, 113, 113, 0.9),
                                stop:1 rgba(239, 68, 68, 0.9));
    border: 2px solid #ef4444;
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
}

QPushButton:pressed {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(220, 38, 38, 0.9),
                                stop:1 rgba(185, 28, 28, 0.9));
}
"""

CREDIT_DISPLAY_STYLE = """
QLabel {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(30, 64, 175, 0.9),
                                stop:1 rgba(29, 78, 216, 0.9));
    border: 3px solid rgba(59, 130, 246, 0.5);
    border-radius: 15px;
    color: white;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 48px;
    font-weight: bold;
    padding: 20px;
    text-align: center;
}
"""

HEADER_STYLE = """
QLabel {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00ff88, stop:0.5 #0088ff, stop:1 #ff0088);
    border-radius: 15px;
    color: #000000;
    font-family: 'Arial Black', 'Impact', sans-serif;
    font-size: 28px;
    font-weight: bold;
    padding: 20px;
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}
"""

GRID_HEADER_STYLE = """
QLabel {
    background: rgba(255, 255, 255, 0.1);
    border-bottom: 3px solid #00ff88;
    color: #ffffff;
    font-size: 22px;
    font-weight: bold;
    padding: 15px;
    text-align: center;
}
"""

# ========== ANIMATION KEYFRAMES ==========
ANIMATION_CSS = """
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

@keyframes glow {
    0% { box-shadow: 0 0 5px #00ff88; }
    50% { box-shadow: 0 0 20px #00ff88, 0 0 30px #0088ff; }
    100% { box-shadow: 0 0 5px #00ff88; }
}

@keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.pulse-animation {
    animation: pulse 2s infinite;
}

.glow-animation {
    animation: glow 1.5s infinite;
}

.slide-in {
    animation: slideIn 0.5s ease-out;
}
"""

# ========== COLOR PALETTE ==========
COLORS = {
    'primary': '#00ff88',      # Neon green
    'secondary': '#0088ff',    # Electric blue
    'accent': '#ff0088',       # Hot pink
    'background': '#0a0a0f',   # Deep space black
    'surface': '#1a1a2e',      # Dark blue surface
    'text': '#ffffff',         # White text
    'text_secondary': '#b0b0b0', # Gray text
    'success': '#00ff88',      # Success green
    'warning': '#ffaa00',      # Warning orange
    'error': '#ff4444',        # Error red
    'gold': '#ffd700',         # Gold for money
    'purple': '#9333ea',       # Purple for credit card
}
