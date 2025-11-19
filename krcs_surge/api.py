import frappe

@frappe.whitelist()
def apply_for_project(project):
    if frappe.session.user == "Guest": frappe.throw("Login required")
    volunteer = frappe.db.get_value("Volunteer", {"user": frappe.session.user}, "name")
    
    if frappe.db.exists("Volunteer Application", {"volunteer": volunteer, "project": project}):
        frappe.throw("Already applied.")

    doc = frappe.get_doc({
        "doctype": "Volunteer Application",
        "volunteer": volunteer,
        "project": project,
        "status": "Pending",
        "date": frappe.utils.today()
    })
    doc.insert(ignore_permissions=True)
    return "Success"