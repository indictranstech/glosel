// Copyright (c) 2016, New Indictrans Technologies PVT LTD and contributors
// For license information, please see license.txt


cur_frm.add_fetch("post_code", "city", "city");
cur_frm.add_fetch("post_code", "state", "state");
cur_frm.add_fetch("post_code", "area", "area");

frappe.ui.form.on('Post Code Cluster', {
	refresh: function(frm) {

	}
});
