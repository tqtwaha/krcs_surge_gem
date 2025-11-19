import frappe
import requests
import base64
from datetime import datetime

def get_mpesa_auth_token():
    settings = frappe.get_single("MPesa Settings")
    consumer_key = settings.consumer_key
    consumer_secret = settings.consumer_secret
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        frappe.throw("Failed to authenticate with M-Pesa")

@frappe.whitelist()
def trigger_stk_push(phone_number, amount, account_reference, transaction_desc):
    token = get_mpesa_auth_token()
    settings = frappe.get_single("MPesa Settings")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = f"{settings.business_shortcode}{settings.passkey}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode('utf-8')
    
    payload = {
        "BusinessShortCode": settings.business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.business_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": f"{frappe.utils.get_url()}/api/method/krcs_surge.integrations.mpesa_utils.mpesa_callback",
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    
    headers = { "Authorization": f"Bearer {token}" }
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

@frappe.whitelist()
def pay_volunteer_via_mpesa(expense_claim_id):
    if not frappe.get_roles(frappe.session.user).count("Accounts User"):
        frappe.throw("Not authorized.")
        
    claim = frappe.get_doc("Expense Claim", expense_claim_id)
    if claim.status != "Approved": frappe.throw("Claim must be Approved.")
    
    settings = frappe.get_single("MPesa Settings")
    token = get_mpesa_auth_token()
    volunteer_phone = frappe.db.get_value("Employee", claim.employee, "cell_number")
    
    payload = {
        "InitiatorName": settings.initiator_name,
        "SecurityCredential": settings.security_credential,
        "CommandID": "BusinessPayment",
        "Amount": claim.total_sanctioned_amount,
        "PartyA": settings.business_shortcode,
        "PartyB": volunteer_phone,
        "Remarks": f"Exp Claim {claim.name}",
        "QueueTimeOutURL": f"{frappe.utils.get_url()}/api/method/krcs_surge.integrations.mpesa_utils.b2c_timeout",
        "ResultURL": f"{frappe.utils.get_url()}/api/method/krcs_surge.integrations.mpesa_utils.b2c_callback"
    }
    
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = { "Authorization": f"Bearer {token}" }
    response = requests.post(api_url, json=payload, headers=headers)
    
    res_data = response.json()
    if "ConversationID" in res_data:
        claim.custom_mpesa_reference = res_data["ConversationID"]
        claim.save()
        return {"status": "queued", "message": "Payment queued."}
    else:
        frappe.throw(f"M-Pesa Error: {res_data.get('errorMessage')}")

@frappe.whitelist(allow_guest=True)
def mpesa_callback(**kwargs):
    data = frappe.request.get_json()
    pass