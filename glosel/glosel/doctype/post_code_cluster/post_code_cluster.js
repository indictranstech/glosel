// Copyright (c) 2016, New Indictrans Technologies PVT LTD and contributors
// For license information, please see license.txt


cur_frm.add_fetch("post_code", "city", "city");
cur_frm.add_fetch("post_code", "state", "state");
cur_frm.add_fetch("post_code", "area", "area");
cur_frm.add_fetch("sales_person", "employee", "employee");

frappe.ui.form.on('Post Code Cluster', {
	refresh: function(frm) {

	},
	validate: function(frm, cdt,cdn){
		if(frm.doc.sales_person_table){
			for(i=0;i<frm.doc.sales_person_table.length;i++){
			// msgprint(frm.doc.sales_person_table[i].sales_person)
				abc = add_share(frm.doc.sales_person_table[i].employee,cdt,cdn)
				b = JSON.parse(abc["responseText"])
				frm.doc.sales_person_table[i].user_id = b.message.user_id; 
			}
		}
	},
});

add_share = function(employee,cdt,cd){
			return frappe.call({
		       method: "frappe.client.get_value",
		       async:false,
		       args: {
		           doctype: "Employee",
		           fieldname: "user_id",
		           filters: { name: employee },
		       },
		      	callback: function(res){
		         	if (res && res.message){
		         		 console.log(res.message['user_id']);
		         		 // return res.message['user_id'];
		          	}
		      	}  	
		   });
}
