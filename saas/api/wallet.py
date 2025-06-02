import frappe
from frappe.utils import now_datetime

def create_wallet_on_user_creation(doc, method):
    if not frappe.db.exists("Wallet", {"user": doc.name}):
        wallet = frappe.get_doc({
            "doctype": "Wallet",
            "user": doc.name,
            "balance": 0
        })
        wallet.insert()

@frappe.whitelist()
def top_up_wallet(wallet, amount):
    amount = float(amount)

    wallet_doc = frappe.get_doc("Wallet", wallet)

    # Add transaction to history
    wallet_doc.append("wallet_transactions", {
        "date": now_datetime(),
        "amount": amount,
        "description": "Top-Up"
    })

    # Update balance and last transaction
    wallet_doc.balance += amount
    wallet_doc.last_transaction = now_datetime()
    wallet_doc.save()
    frappe.db.commit()

    return "Wallet topped up successfully!"

@frappe.whitelist()
def deduct_wallet(wallet, amount):
    amount = float(amount)
    wallet_doc = frappe.get_doc("Wallet", wallet)

    if wallet_doc.balance < amount:
        frappe.throw("Insufficient balance!")

    wallet_doc.append("wallet_transactions", {
        "date": now_datetime(),
        "amount": -amount,
        "description": "Deduction"
    })

    wallet_doc.balance -= amount
    wallet_doc.last_transaction = now_datetime()
    wallet_doc.save()
    frappe.db.commit()

    return "Amount deducted successfully!"

@frappe.whitelist()
def buy_subscription(wallet, amount):
    # Same logic, just change description
    amount = float(amount)
    wallet_doc = frappe.get_doc("Wallet", wallet)

    if wallet_doc.balance < amount:
        frappe.throw("Insufficient balance!")

    wallet_doc.append("wallet_transactions", {
        "date": now_datetime(),
        "amount": -amount,
        "description": "Buy Subscription"
    })

    wallet_doc.balance -= amount
    wallet_doc.last_transaction = now_datetime()
    wallet_doc.save()
    frappe.db.commit()

    return "Subscription purchased successfully!"

