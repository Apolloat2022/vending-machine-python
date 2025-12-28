"""
main_web.py - Web version for Render deployment
"""

from flask import Flask, render_template_string, request, jsonify, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'vendor-pro-2026-cinematic-secret'

# Simple in-memory vending machine for web
class WebVendingMachine:
    def __init__(self):
        self.balance = 0.0
        self.total_sales = 0.0
        self.transactions = []
        self.products = {}
        self.load_products()
    
    def load_products(self):
        """Load products for web version"""
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
            self.products[code] = {
                'code': code,
                'name': name,
                'price': price,
                'quantity': quantity,
                'available': quantity > 0
            }
    
    def insert_cash(self, amount):
        """Insert cash"""
        if amount <= 0:
            return False, "Invalid amount"
        
        self.balance += amount
        self.log_transaction(f"Cash inserted: ${amount:.2f}")
        return True, f"Added ${amount:.2f}"
    
    def purchase(self, product_code):
        """Purchase a product"""
        if product_code not in self.products:
            return False, "Invalid product code"
        
        product = self.products[product_code]
        
        if product['quantity'] <= 0:
            return False, f"Sorry, {product['name']} is out of stock!"
        
        if self.balance < product['price']:
            return False, f"Insufficient funds! Need: ${product['price']:.2f}"
        
        # Process purchase
        product['quantity'] -= 1
        change = self.balance - product['price']
        self.total_sales += product['price']
        self.balance = 0.0
        
        self.log_transaction(f"Purchased {product['name']} for ${product['price']:.2f}")
        return True, {
            'product': product['name'],
            'change': change,
            'message': f"Enjoy your {product['name']}!"
        }
    
    def cancel_transaction(self):
        """Cancel and return balance"""
        change = self.balance
        self.balance = 0.0
        if change > 0:
            self.log_transaction(f"Cancelled. Returned: ${change:.2f}")
        return change
    
    def log_transaction(self, message):
        """Log transaction"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"{timestamp}: {message}")
    
    def get_state(self):
        """Get current machine state"""
        return {
            'balance': self.balance,
            'total_sales': self.total_sales,
            'products': self.products,
            'transactions': self.transactions[-10:]  # Last 10
        }

# Initialize vending machine
vm = WebVendingMachine()

# HTML template for web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vendor Pro 2026 - Web Edition</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(90deg, #00ff88, #0088ff, #ff0088);
            border-radius: 15px;
            color: #000;
        }
        
        .header h1 {
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-content {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        @media (max-width: 1024px) {
            .main-content {
                flex-direction: column;
            }
        }
        
        .left-panel, .right-panel {
            background: rgba(30, 30, 46, 0.9);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        .left-panel {
            flex: 1;
            max-width: 350px;
        }
        
        .right-panel {
            flex: 2;
        }
        
        .credit-display {
            background: linear-gradient(135deg, #1e40af, #1d4ed8);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            border: 3px solid rgba(59, 130, 246, 0.5);
        }
        
        .credit-amount {
            font-size: 3em;
            font-weight: bold;
            font-family: 'Consolas', monospace;
            color: white;
        }
        
        .money-buttons {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .money-btn, .action-btn {
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            color: white;
        }
        
        .money-btn {
            background: linear-gradient(135deg, #4CAF50, #388E3C);
        }
        
        .money-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        }
        
        .action-buttons {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .card-btn {
            background: linear-gradient(135deg, #9333ea, #4f46e5);
        }
        
        .eject-btn {
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }
        
        .admin-btn {
            background: linear-gradient(135deg, #64748b, #475569);
        }
        
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .product-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        
        @media (max-width: 768px) {
            .product-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        .product-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            border: 2px solid rgba(0, 255, 136, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .product-card:hover {
            background: rgba(0, 255, 136, 0.2);
            border-color: #00ff88;
            transform: translateY(-5px);
        }
        
        .product-card.out-of-stock {
            border-color: rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.05);
            color: #888;
            cursor: not-allowed;
        }
        
        .product-card.out-of-stock:hover {
            transform: none;
            background: rgba(255, 255, 255, 0.05);
        }
        
        .product-name {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 5px;
        }
        
        .product-price {
            color: #00ff88;
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 5px;
        }
        
        .product-quantity {
            color: #888;
            font-size: 0.9em;
        }
        
        .status-bar {
            background: rgba(0, 0, 0, 0.9);
            border-top: 2px solid #00ff88;
            padding: 10px;
            border-radius: 0 0 10px 10px;
            font-weight: bold;
            color: #00ff88;
            text-align: center;
        }
        
        .messages {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .message {
            background: linear-gradient(135deg, #00ff88, #0088ff);
            color: #000;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            animation: slideIn 0.5s ease;
            font-weight: bold;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .emoji {
            font-size: 1.5em;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 VENDOR PRO 2026 - WEB EDITION 🎬</h1>
        </div>
        
        <div class="main-content">
            <!-- Left Panel -->
            <div class="left-panel">
                <div class="credit-display">
                    <div style="font-size: 1.2em; margin-bottom: 10px;">💰 AVAILABLE CREDIT</div>
                    <div class="credit-amount" id="creditAmount">${{ "%.2f"|format(vm.balance) }}</div>
                </div>
                
                <h3 style="margin-bottom: 15px; color: #00ff88;">💸 ADD MONEY</h3>
                <div class="money-buttons">
                    <button class="money-btn" onclick="addMoney(5)">➕ $5</button>
                    <button class="money-btn" onclick="addMoney(1)">➕ $1</button>
                    <button class="money-btn" onclick="addMoney(0.25)">➕ $0.25</button>
                    <button class="money-btn" onclick="addMoney(0.1)">➕ $0.10</button>
                    <button class="money-btn" onclick="addMoney(0.05)">➕ $0.05</button>
                    <button class="money-btn" onclick="addMoney(20)">➕ $20</button>
                </div>
                
                <div class="action-buttons">
                    <button class="action-btn card-btn" onclick="showCreditCard()">
                        💳 CINEMATIC CARD PAYMENT
                    </button>
                    <button class="action-btn eject-btn" onclick="ejectChange()">
                        🔄 EJECT CHANGE
                    </button>
                    <button class="action-btn admin-btn" onclick="showAdmin()">
                        ⚙️ CINEMATIC ADMIN
                    </button>
                </div>
            </div>
            
            <!-- Right Panel -->
            <div class="right-panel">
                <h2 style="margin-bottom: 20px; text-align: center; color: #00ff88;">
                    🎯 PRODUCT SELECTION 🎯
                </h2>
                
                <div class="product-grid" id="productGrid">
                    {% for code, product in vm.products.items() %}
                    <div class="product-card {% if product.quantity <= 0 %}out-of-stock{% endif %}" 
                         onclick="purchaseProduct('{{ code }}')">
                        <div class="product-name">{{ product.name }}</div>
                        <div class="product-price">${{ "%.2f"|format(product.price) }}</div>
                        <div class="product-quantity">{{ product.quantity }} units available</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="status-bar" id="statusBar">
            🎬 Ready for cinematic vending experience!
        </div>
    </div>
    
    <!-- Messages Area -->
    <div class="messages" id="messages"></div>
    
    <script>
        function showMessage(text, type = 'info') {
            const messages = document.getElementById('messages');
            const message = document.createElement('div');
            message.className = 'message';
            message.textContent = text;
            messages.appendChild(message);
            
            // Remove message after 5 seconds
            setTimeout(() => {
                message.remove();
            }, 5000);
        }
        
        function addMoney(amount) {
            fetch('/api/add-money', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ amount: amount })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('creditAmount').textContent = '$' + data.balance.toFixed(2);
                    showMessage('💰 Added $' + amount.toFixed(2) + ' to balance!', 'success');
                    updateStatus('💰 Added $' + amount.toFixed(2) + ' - Ready to purchase!');
                    updateProducts();
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(error => {
                showMessage('Error: ' + error, 'error');
            });
        }
        
        function purchaseProduct(code) {
            fetch('/api/purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_code: code })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('creditAmount').textContent = '$' + data.balance.toFixed(2);
                    showMessage('🎉 ' + data.message, 'success');
                    updateStatus('🎉 Enjoy your ' + data.product_name + '!');
                    updateProducts();
                    
                    if (data.change > 0) {
                        setTimeout(() => {
                            showMessage('💵 Change: $' + data.change.toFixed(2), 'info');
                        }, 1000);
                    }
                } else {
                    showMessage('⚠️ ' + data.message, 'error');
                    updateStatus('⚠️ ' + data.message);
                }
            })
            .catch(error => {
                showMessage('Error: ' + error, 'error');
            });
        }
        
        function ejectChange() {
            fetch('/api/cancel', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('creditAmount').textContent = '$' + data.balance.toFixed(2);
                if (data.change > 0) {
                    showMessage('💸 Change ejected: $' + data.change.toFixed(2), 'success');
                    updateStatus('💸 Change ejected: $' + data.change.toFixed(2));
                } else {
                    showMessage('No money to return', 'info');
                    updateStatus('No money to return');
                }
            });
        }
        
        function showCreditCard() {
            const amount = prompt('Enter credit card payment amount ($):', '10.00');
            if (amount && !isNaN(amount) && parseFloat(amount) > 0) {
                fetch('/api/credit-card', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ amount: parseFloat(amount) })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('creditAmount').textContent = '$' + data.balance.toFixed(2);
                        showMessage('💳 Card payment: $' + amount + ' added!', 'success');
                        updateStatus('💳 Card payment: $' + amount + ' added!');
                        updateProducts();
                    } else {
                        showMessage(data.message, 'error');
                    }
                });
            }
        }
        
        function showAdmin() {
            fetch('/api/admin')
            .then(response => response.json())
            .then(data => {
                alert('🎬 CINEMATIC ADMIN PANEL\n\n' +
                      '💰 Total Sales: $' + data.total_sales.toFixed(2) + '\n' +
                      '📦 Total Products: ' + data.total_products + '\n' +
                      '🔄 Restock Available\n' +
                      '📊 View Transaction Logs\n\n' +
                      'Password: cinematic2026');
            });
        }
        
        function updateStatus(message) {
            document.getElementById('statusBar').textContent = message;
        }
        
        function updateProducts() {
            // In a real app, you would refresh the product grid
            // For simplicity, we'll just reload the page
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
        
        // Initial status
        updateStatus('🎬 Ready for cinematic vending experience!');
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE, vm=vm)

@app.route('/api/add-money', methods=['POST'])
def api_add_money():
    """API to add money"""
    data = request.json
    amount = float(data.get('amount', 0))
    
    success, message = vm.insert_cash(amount)
    
    return jsonify({
        'success': success,
        'message': message,
        'balance': vm.balance
    })

@app.route('/api/purchase', methods=['POST'])
def api_purchase():
    """API to purchase product"""
    data = request.json
    product_code = data.get('product_code', '')
    
    success, result = vm.purchase(product_code)
    
    if success:
        return jsonify({
            'success': True,
            'message': result['message'],
            'product_name': result['product'],
            'change': result['change'],
            'balance': vm.balance
        })
    else:
        return jsonify({
            'success': False,
            'message': result,
            'balance': vm.balance
        })

@app.route('/api/cancel', methods=['POST'])
def api_cancel():
    """API to cancel transaction"""
    change = vm.cancel_transaction()
    
    return jsonify({
        'success': True,
        'change': change,
        'balance': vm.balance
    })

@app.route('/api/credit-card', methods=['POST'])
def api_credit_card():
    """API for credit card payment"""
    data = request.json
    amount = float(data.get('amount', 0))
    
    # Mock credit card processing
    if amount <= 0:
        return jsonify({
            'success': False,
            'message': 'Invalid amount'
        })
    
    vm.balance += amount
    vm.log_transaction(f"Credit card payment: ${amount:.2f}")
    
    return jsonify({
        'success': True,
        'message': f'Card payment of ${amount:.2f} processed',
        'balance': vm.balance
    })

@app.route('/api/admin', methods=['GET'])
def api_admin():
    """API for admin info"""
    return jsonify({
        'total_sales': vm.total_sales,
        'total_products': len(vm.products),
        'transactions': vm.transactions[-5:]  # Last 5 transactions
    })

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """API to reset machine (admin only)"""
    # In production, add authentication
    vm.__init__()  # Reset to initial state
    return jsonify({
        'success': True,
        'message': 'Machine reset to initial state'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
