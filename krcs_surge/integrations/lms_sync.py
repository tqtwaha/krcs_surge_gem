import frappe
from frappe.utils import today

def on_certificate_issued(doc, method):
    user_email = doc.member 
    volunteer_name = frappe.db.get_value("Volunteer", {"user": user_email}, "name")
    
    if not volunteer_name: return

    volunteer = frappe.get_doc("Volunteer", volunteer_name)
    volunteer.append("certifications", {
        "course": doc.course,
        "certificate_number": doc.name,
        "issue_date": doc.issue_date or today(),
        "expiry_date": doc.expiry_date,
        "certificate_url": doc.attachment
    })
    
    induction_course_name = frappe.db.get_single_value("KRCS Settings", "induction_course")
    if doc.course == induction_course_name and volunteer.status == "Onboarding":
        volunteer.status = "Active"
        
    volunteer.save(ignore_permissions=True)