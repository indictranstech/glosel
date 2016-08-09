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
frappe.ui.form.on("Scheme Management", "valid_from", function(frm) {
	console.log(cur_frm.doc.valid_from < frappe.datetime.nowdate())
  
  if (cur_frm.doc.valid_froms < frappe.datetime.nowdate())
  {
    frappe.throw(__("Date can't be less than Today's date"));
  }

});