"""
main.py - Entry point for cinematic vending machine
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.views import CinematicMainWindow
    print("✓ CinematicMainWindow imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import...")
    from views import CinematicMainWindow

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set modern font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = CinematicMainWindow()
    window.show()
    
    print("🎬 VENDOR PRO 2026 - CINEMATIC EDITION 🎬")
    print("=" * 50)
    print("Features:")
    print("• Dark cinematic theme with neon accents")
    print("• Modern glass-morphism effects")
    print("• Animated interactions")
    print("• Credit card payment support")
    print("• 24 products with emojis")
    print("=" * 50)
    
    # Start application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
