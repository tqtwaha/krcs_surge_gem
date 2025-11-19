import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect

    volunteer_name = frappe.db.get_value("Volunteer", {"user": frappe.session.user}, "name")
    if not volunteer_name:
        context.no_profile = True
        return context

    volunteer_doc = frappe.get_doc("Volunteer", volunteer_name)
    user_branch = volunteer_doc.branch
    
    context.projects = frappe.db.get_all(
        "Project",
        filters={
            "status": "Open",
            "percent_complete": ["<", 100],
            "or_filters": [
                {"company": user_branch},
                {"custom_is_national": 1} 
            ]
        },
        fields=["name", "project_name", "expected_end_date", "company", "project_type", "description"]
    )
    context.volunteer = volunteer_doc