frappe.ui.form.on('Expense Claim', {
    refresh: function(frm) {
        if (frm.doc.status === 'Approved' && frm.doc.docstatus === 1 && !frm.doc.is_paid) {
            frm.add_custom_button(__('Pay via M-Pesa'), function() {
                frappe.confirm('Send KES ' + frm.doc.total_sanctioned_amount + '?', function() {
                    frappe.call({
                        method: 'krcs_surge.integrations.mpesa_utils.pay_volunteer_via_mpesa',
                        args: { expense_claim_id: frm.doc.name },
                        freeze: true,
                        callback: function(r) { if (!r.exc) { frappe.msgprint(r.message); frm.reload_doc(); } }
                    });
                });
            }).addClass("btn-primary");
        }
    }
});