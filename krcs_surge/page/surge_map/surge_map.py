import frappe
@frappe.whitelist()
def get_county_data():
    data = frappe.db.sql("SELECT county, COUNT(name) FROM `tabVolunteer` WHERE status = 'Active' GROUP BY county", as_list=1)
    return dict(data)