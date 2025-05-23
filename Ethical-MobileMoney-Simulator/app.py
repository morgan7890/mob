from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)
TRANSACTION_LOG = "transactions.json"

# Load existing transactions
def load_transactions():
    try:
        with open(TRANSACTION_LOG, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save transactions
def save_transaction(data):
    transactions = load_transactions()
    transactions.append(data)
    with open(TRANSACTION_LOG, "w") as f:
        json.dump(transactions, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        action = request.form["action"]
        amount = float(request.form["amount"])
        apply_fee = "apply_fee" in request.form

        fee = 1.5 if apply_fee else 0
        final_amount = amount - fee if action == "withdraw" else amount

        tx = {
            "name": name,
            "action": action,
            "original_amount": amount,
            "final_amount": final_amount,
            "fee": fee,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        save_transaction(tx)
        return redirect("/")

    transactions = load_transactions()
    return render_template("index.html", transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
