// Copyright (c) 2016, New Indictrans Technologies PVT LTD and contributors
// For license information, please see license.txt


cur_frm.add_fetch("post_code", "city", "city");
cur_frm.add_fetch("post_code", "state", "state");
cur_frm.add_fetch("post_code", "area", "area");
cur_frm.add_fetch("sales_person", "employee", "employee");

frappe.ui.form.on('Post Code Cluster', {
	refresh: function(frm) {

	},
	validate: function(frm){
		msgprint("hi");
		for(i=0;i<frm.doc.sales_person_table.length;i++){
			msgprint(frm.doc.sales_person_table[i].sales_person)
		}
	}
});
