// Copyright (c) 2016, New Indictrans Technologies PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scheme Management', {
	refresh: function(frm) {

	}
});

cur_frm.fields_dict.customer.get_query = function(doc){
	return {
		query:"glosel.custom_py_methods.customer_filter"
	}
}