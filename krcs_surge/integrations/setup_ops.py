import frappe

def create_branch_warehouse(doc, method):
    if not doc.parent_company: return

    warehouse_name = f"Main Store - {doc.company_abbr}"
    if frappe.db.exists("Warehouse", warehouse_name): return

    new_warehouse = frappe.get_doc({
        "doctype": "Warehouse",
        "warehouse_name": warehouse_name,
        "company": doc.name,
        "parent_warehouse": "All Warehouses - " + doc.company_abbr,
        "is_group": 0,
        "account": f"Stock Assets - {doc.company_abbr}"
    })
    new_warehouse.insert(ignore_permissions=True)