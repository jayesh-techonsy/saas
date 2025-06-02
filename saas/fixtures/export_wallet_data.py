import frappe
import json
from datetime import datetime, date

def convert_datetime(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@frappe.whitelist()
def export_wallet_fixtures():
    data = {}

    for doctype in [
        "Wallet",
        "Wallet Transaction",
        "My Subscription",
        "All Subscription Plans"
    ]:
        records = frappe.get_all(doctype, fields="*")
        data[doctype] = records

    file_path = frappe.get_app_path("saas", "fixtures", "wallet_fixtures.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4, default=convert_datetime)

    frappe.msgprint(f"Exported wallet-related data to {file_path}")

