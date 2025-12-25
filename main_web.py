from flask import Flask, render_template, request, redirect, url_for
from src.models import VendingMachine, Product
import os

app = Flask(__name__)
vm = VendingMachine()

data_path = os.path.join('data', 'inventory.json')
if not vm.load_inventory(data_path):
    # Fallback to ensure the web demo has items
    vm.add_product(Product("Coke", 1.75, 10, "A1"))
    vm.save_inventory(data_path)

@app.route('/')
def index():
    return render_template('index.html', inventory=vm.inventory, balance=vm.balance)

@app.route('/insert', methods=['POST'])
def insert():
    amount = float(request.form.get('amount', 0))
    vm.insert_money(amount)
    return redirect(url_for('index'))

@app.route('/buy/<code>')
def buy(code):
    success, msg, price = vm.purchase_product(code)
    if success:
        vm.save_inventory(data_path)
        vm.log_transaction(vm.inventory[code].name, price)
    return redirect(url_for('index'))

@app.route('/refund')
def refund():
    vm.refund()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("\n--- SERVER STARTING ---")
    print("Go to: http://127.0.0.1:5000")
    print("-----------------------\n")
    app.run(debug=True)
