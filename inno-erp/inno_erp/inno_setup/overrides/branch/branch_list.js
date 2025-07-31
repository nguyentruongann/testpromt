
frappe.listview_settings['Branch'] = {
    add_fields: ['custom_disabled'],
    
    get_indicator: function(doc) {
        if (doc.custom_disabled === 1) {
            return [__("Disabled"), "gray", "custom_disabled,=,1"];
        } 
        if (doc.custom_disabled === 0) {
            return [__("Enabled"), "blue", "custom_disabled,=,0"];
        }
        
    },

};