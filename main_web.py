"""
main_web.py - Web version for Render deployment (FIXED VERSION)
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
        """Purchase a product - Subtracts cost but keeps remaining balance!"""
        if product_code not in self.products:
            return False, "Invalid product code"
        
        product = self.products[product_code]
        
        if product['quantity'] <= 0:
            return False, f"Sorry, {product['name']} is out of stock!"
        
        if self.balance < product['price']:
            return False, f"Insufficient funds! Need: ${product['price']:.2f}"
        
        # Process purchase
        product['quantity'] -= 1
        # LOGIC FIX: Do NOT reset balance to 0. Just subtract the price.
        self.balance -= product['price']
        self.total_sales += product['price']
        
        self.log_transaction(f"Purchased {product['name']} for ${product['price']:.2f}")
        return True, {
            'product': product['name'],
            'price': product['price'],
            'new_balance': self.balance,
            'message': f"Dispensed {product['name']}!"
        }
    
    def cancel_transaction(self):
        """Cancel and return balance"""
        change = self.balance
        self.balance = 0.0
        if change > 0:
            self.log_transaction(f"Change dispensed: ${change:.2f}")
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

# HTML template for web interface - CYBERPUNK GOLD EDITION
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vendor Pro 2026 | Premium Access</title>
    <style>
        :root {
            --gold: #FFD700;
            --gold-dim: #b39700;
            --gold-glow: rgba(255, 215, 0, 0.4);
            --bg: #050510;
            --glass: rgba(255, 255, 255, 0.03);
            --text-main: #ffffff;
            --success: #00ff88;
            --error: #ff4444;
        }

        * {
            box-sizing: border-box;
            transition: all 0.2s ease;
        }

        body { 
            background: radial-gradient(circle at center, #101025 0%, var(--bg) 100%);
            color: var(--text-main); 
            font-family: 'Segoe UI', system-ui, sans-serif; 
            margin: 0; 
            padding: 20px; 
            min-height: 100vh;
            display: flex; 
            flex-direction: column; 
            align-items: center;
        }

        /* Animated Header */
        h1 { 
            font-size: 2.5rem; 
            letter-spacing: 5px; 
            margin-bottom: 30px;
            background: linear-gradient(to right, #fff, var(--gold), #fff);
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            text-transform: uppercase; 
            text-shadow: 0 0 20px var(--gold-glow);
            text-align: center;
        }

        /* Main Glass Dashboard */
        .dashboard {
            display: flex;
            gap: 30px;
            background: var(--glass);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,215,0,0.2);
            border-radius: 24px;
            padding: 40px;
            width: 100%; 
            max-width: 1400px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        .panel-left {
            flex: 1;
            max-width: 350px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .panel-right {
            flex: 3;
        }

        /* Credit Display */
        .credit-box {
            background: rgba(0,0,0,0.4);
            border: 2px solid var(--gold);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.1);
        }
        
        .credit-label { font-size: 0.8rem; text-transform: uppercase; color: #aaa; letter-spacing: 2px; }
        .credit-amount { 
            font-size: 3rem; 
            font-weight: 800; 
            color: var(--gold); 
            margin: 10px 0; 
            font-family: 'Consolas', monospace;
            text-shadow: 0 0 10px var(--gold-glow);
        }

        /* Control Buttons */
        .btn-group {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .btn { 
            background: rgba(255, 215, 0, 0.1); 
            border: 1px solid var(--gold); 
            color: var(--gold);
            padding: 15px; 
            border-radius: 12px; 
            font-weight: bold; 
            cursor: pointer;
            text-transform: uppercase; 
            font-size: 0.9rem; 
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        
        .btn:hover { 
            background: var(--gold); 
            color: black; 
            box-shadow: 0 0 20px var(--gold-glow); 
            transform: translateY(-2px); 
        }

        .btn:active {
            transform: scale(0.98);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-full { grid-column: span 2; }
        
        .btn-refund { 
            border-color: #ff4444; 
            color: #ff4444; 
            background: rgba(255, 68, 68, 0.1); 
        }
        .btn-refund:hover { 
            background: #ff4444; 
            color: white; 
            box-shadow: 0 0 20px rgba(255,68,68,0.4); 
        }

        .btn-card {
            border-color: #70a1ff;
            color: #70a1ff;
            background: rgba(112, 161, 255, 0.1);
        }
        .btn-card:hover {
            background: #70a1ff;
            color: black;
            box-shadow: 0 0 20px rgba(112, 161, 255, 0.4);
        }

        /* Product Grid */
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); 
            gap: 20px;
        }

        .item-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            display: flex; 
            flex-direction: column; 
            align-items: center;
            cursor: pointer;
            position: relative;
        }

        .item-card:hover:not(.disabled) {
            border-color: var(--gold);
            background: rgba(255, 215, 0, 0.05);
            transform: scale(1.05);
            box-shadow: 0 0 25px rgba(255,215,0,0.15);
        }

        .item-card.disabled {
            opacity: 0.5;
            cursor: not-allowed;
            pointer-events: none;
        }

        .item-code {
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 0.7rem;
            color: #666;
            font-weight: bold;
        }

        .item-name { 
            font-weight: 700; 
            font-size: 1rem; 
            margin: 15px 0 10px 0; 
            text-align: center; 
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .item-price { 
            color: var(--gold); 
            font-weight: bold; 
            font-size: 1.2rem; 
        }
        
        .item-stock { 
            font-size: 0.7rem; 
            color: #888; 
            margin-top: 10px; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
        }

        /* Toast Notifications */
        .messages {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .message {
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            border-left: 5px solid var(--gold);
            animation: slideIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            min-width: 300px;
        }
        
        .message.success { border-left-color: var(--success); }
        .message.error { border-left-color: var(--error); }

        @keyframes slideIn {
            from { transform: translateX(120%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @media (max-width: 900px) {
            .dashboard { flex-direction: column; }
            .panel-left { max-width: 100%; }
        }
        
        /* Terminal/Console Output for Status */
        .status-terminal {
            margin-top: 20px;
            background: #000;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Consolas', monospace;
            color: var(--success);
            font-size: 0.9rem;
            height: 40px;
            display: flex;
            align-items: center;
            overflow: hidden;
            white-space: nowrap;
        }
    </style>
</head>
<body>
    <h1>Vendor Pro 2026</h1>

    <div class="dashboard">
        <!-- LEFT CONTROL PANEL -->
        <div class="panel-left">
            <div class="credit-box">
                <div class="credit-label">Available Credit</div>
                <div class="credit-amount" id="creditAmount">${{ "%.2f"|format(vm.balance) }}</div>
            </div>
            
            <div class="btn-group">
                <button class="btn" id="btn-1">+ $1.00</button>
                <button class="btn" id="btn-5">+ $5.00</button>
                <button class="btn" id="btn-quarter">+ $0.25</button>
                <button class="btn" id="btn-10">+ $10.00</button>
                
                <button class="btn btn-card btn-full" id="btn-card">
                    💳 Swipe Card
                </button>
                
                <button class="btn btn-refund btn-full" id="btn-refund">
                    ↩ Eject Change
                </button>
            </div>
            
            <div class="status-terminal" id="statusBar">
                > System Ready...
            </div>
        </div>

        <!-- RIGHT PRODUCT PANEL -->
        <div class="panel-right">
            <div class="grid" id="productGrid">
                {% for code, product in vm.products.items() %}
                <div class="item-card {% if product.quantity <= 0 %}disabled{% endif %}" 
                     data-code="{{ code }}"
                     data-stock="{{ product.quantity }}">
                    <span class="item-code">{{ code }}</span>
                    <span class="item-name">{{ product.name }}</span>
                    <span class="item-price">${{ "%.2f"|format(product.price) }}</span>
                    <span class="item-stock">
                        {% if product.quantity > 0 %}
                            {{ product.quantity }} In Stock
                        {% else %}
                            SOLD OUT
                        {% endif %}
                    </span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="messages" id="messages"></div>

    <script>
        // Wait for DOM to be fully loaded
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Vendor Pro 2026 - Initializing...');
            
            // Attach event listeners to buttons
            document.getElementById('btn-1').addEventListener('click', function() { addMoney(1.00); });
            document.getElementById('btn-5').addEventListener('click', function() { addMoney(5.00); });
            document.getElementById('btn-quarter').addEventListener('click', function() { addMoney(0.25); });
            document.getElementById('btn-10').addEventListener('click', function() { addMoney(10.00); });
            document.getElementById('btn-card').addEventListener('click', showCreditCard);
            document.getElementById('btn-refund').addEventListener('click', ejectChange);
            
            // Attach click handlers to product cards
            const productCards = document.querySelectorAll('.item-card');
            productCards.forEach(card => {
                card.addEventListener('click', function() {
                    const code = this.getAttribute('data-code');
                    const stock = parseInt(this.getAttribute('data-stock'));
                    
                    if (stock > 0) {
                        purchaseProduct(code);
                    }
                });
            });
            
            console.log('System ready!');
        });
        
        function showMessage(text, type = 'info') {
            const container = document.getElementById('messages');
            const msg = document.createElement('div');
            msg.className = 'message ' + type;
            msg.textContent = text;
            container.appendChild(msg);
            
            setTimeout(() => {
                msg.style.opacity = '0';
                msg.style.transform = 'translateY(-20px)';
                setTimeout(() => msg.remove(), 300);
            }, 3000);
        }
        
        function updateDisplay(balance) {
            document.getElementById('creditAmount').textContent = '$' + balance.toFixed(2);
        }
        
        function setStatus(text) {
            document.getElementById('statusBar').textContent = '> ' + text;
        }

        function addMoney(amount) {
            console.log('Adding money:', amount);
            
            fetch('/api/add-money', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ amount: amount })
            })
            .then(res => {
                if (!res.ok) throw new Error('Network error');
                return res.json();
            })
            .then(data => {
                if (data.success) {
                    updateDisplay(data.balance);
                    showMessage('Accepted: $' + amount.toFixed(2), 'success');
                    setStatus('Credit added. Balance: $' + data.balance.toFixed(2));
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Connection error. Please try again.', 'error');
            });
        }
        
        function purchaseProduct(code) {
            console.log('Purchasing product:', code);
            
            fetch('/api/purchase', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ product_code: code })
            })
            .then(res => {
                if (!res.ok) throw new Error('Network error');
                return res.json();
            })
            .then(data => {
                if (data.success) {
                    updateDisplay(data.balance);
                    showMessage('Dispensing ' + data.product_name + '...', 'success');
                    setStatus('Dispensed ' + data.product_name + '. Remaining: $' + data.balance.toFixed(2));
                    setTimeout(() => location.reload(), 1500);
                } else {
                    showMessage(data.message, 'error');
                    setStatus('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Connection error. Please try again.', 'error');
            });
        }
        
        function ejectChange() {
            console.log('Ejecting change...');
            
            fetch('/api/cancel', { method: 'POST' })
            .then(res => {
                if (!res.ok) throw new Error('Network error');
                return res.json();
            })
            .then(data => {
                updateDisplay(data.balance);
                if (data.change > 0) {
                    showMessage('Change dispensed: $' + data.change.toFixed(2), 'success');
                    setStatus('Refunded $' + data.change.toFixed(2) + '. Thank you!');
                } else {
                    showMessage('No credit to refund.', 'info');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Connection error. Please try again.', 'error');
            });
        }
        
        function showCreditCard() {
            const amount = prompt('💳 SWIPE CARD - Enter amount to authorize ($):', '10.00');
            if (amount && !isNaN(amount) && parseFloat(amount) > 0) {
                console.log('Processing card payment:', amount);
                
                fetch('/api/credit-card', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ amount: parseFloat(amount) })
                })
                .then(res => {
                    if (!res.ok) throw new Error('Network error');
                    return res.json();
                })
                .then(data => {
                    if (data.success) {
                        updateDisplay(data.balance);
                        showMessage('Card Authorized!', 'success');
                        setStatus('Card accepted. Balance: $' + data.balance.toFixed(2));
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Card processing failed. Please try again.', 'error');
                });
            }
        }
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
            'balance': result['new_balance']
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
        'transactions': vm.transactions[-5:]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)