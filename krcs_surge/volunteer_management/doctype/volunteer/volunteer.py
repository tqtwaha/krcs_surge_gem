import frappe
from frappe.model.document import Document
from frappe.utils import random_string

class Volunteer(Document):
    def validate(self):
        if self.phone and self.phone.startswith("0"):
            self.phone = "254" + self.phone[1:]

    def after_insert(self):
        self.create_volunteer_user()

    def create_volunteer_user(self):
        if frappe.db.exists("User", self.email):
            return

        user = frappe.get_doc({
            "doctype": "User",
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "enabled": 1,
            "send_welcome_email": 0,
            "roles": [{"role": "Volunteer"}]
        })
        
        temp_password = random_string(10)
        user.new_password = temp_password
        user.save(ignore_permissions=True)
        self.db_set("user", user.name)
        self.send_welcome_email(temp_password)

    def send_welcome_email(self, password):
        subject = "Welcome to the KRCS Surge System"
        message = f"<p>Dear {self.first_name},</p><p>Login: {self.email}<br>Password: {password}</p>"
        frappe.sendmail(recipients=[self.email], subject=subject, message=message)