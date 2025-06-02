import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def get_all_plans():
    return frappe.get_all("All Subscription Plans", fields=["name", "plan_name", "price", "duration_days"])

@frappe.whitelist()
def subscribe_user(user, plan_name):
    # Fetch user Wallet
    user_wallet = frappe.get_doc("Wallet", {"user": user})
    plan_doc = frappe.get_doc("All Subscription Plans", plan_name)

    if user_wallet.balance < plan_doc.price:
        return "Insufficient balance! Please top up your wallet."

    # Deduct Balance
    user_wallet.balance -= plan_doc.price

    # Add Wallet Transaction
    user_wallet.append("wallet_transactions", {
        "date": frappe.utils.now_datetime(),  # Correct for Datetime field
        "amount": plan_doc.price,
        "description": f"Subscribed to {plan_doc.plan_name}"
    })


    user_wallet.save(ignore_permissions=True)
    frappe.db.commit()

    # Calculate Dates
    start_date = datetime.today().date()
    end_date = start_date + timedelta(days=plan_doc.duration_days)

    # Create record in My Subscription
    subscription = frappe.get_doc({
        "doctype": "My Subscription",
        "user": user,
        "subscription_plan": plan_doc.name,
        "plan_name": plan_doc.plan_name,
        "start_date": start_date,
        "end_date": end_date,
        "status": "Active",
        "price": plan_doc.price
    })
    subscription.insert(ignore_permissions=True)
    frappe.db.commit()

    return f"Subscription to {plan_doc.plan_name} activated successfully!"

