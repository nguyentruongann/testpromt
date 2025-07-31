
frappe.ui.form.on('Coupon Code', {
    refresh: function(frm) {
        frm.set_df_property('pricing_rule', 'hidden', 1);
        frm.set_df_property('pricing_rule', 'reqd', 0);
        frm.set_df_property('valid_from', 'hidden', 1);
        frm.set_df_property('valid_upto', 'hidden', 1);
    },

});
