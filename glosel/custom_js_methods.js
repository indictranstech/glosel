frappe.ui.form.on("Supplier Quotation Item","item_code" ,function(frm,cdt,cdn){
	if (cur_frm.doc.supplier=="")
	{
	frappe.throw(__("Please Enter Supplier Name"))	
	}
	items=locals[cdt][cdn]
	return frappe.call({
			method: "glosel.api.fetch_supplier_uom",
			args: {
				supplier: frm.doc.supplier,
				item:items.item_code
			},
			callback: function(r) {
				if(r.message){
					console.log(r.message)
					console.log(items.unit_of_measure)
					items.unit_of_measure=r.message
					cur_frm.refresh_fields()
				}
			}
		});
})

frappe.ui.form.on("Purchase Order Item","item_code" ,function(frm,cdt,cdn){
	if (cur_frm.doc.supplier=="")
	{
	frappe.throw(__("Please Enter Supplier Name"))	
	}
	items=locals[cdt][cdn]
	return frappe.call({
			method: "glosel.api.fetch_supplier_uom",
			args: {
				supplier: frm.doc.supplier,
				item:items.item_code
			},
			callback: function(r) {
				if(r.message){
					console.log(r.message)
					console.log(items.unit_of_measure)
					items.unit_of_measure=r.message
					cur_frm.refresh_fields()
				}
			}
		});
})

frappe.ui.form.on("Purchase Receipt Item","item_code" ,function(frm,cdt,cdn){
	if (cur_frm.doc.supplier=="")
	{
	frappe.throw(__("Please Enter Supplier Name"))	
	}
	items=locals[cdt][cdn]
	return frappe.call({
			method: "glosel.api.fetch_supplier_uom",
			args: {
				supplier: frm.doc.supplier,
				item:items.item_code
			},
			callback: function(r) {
				if(r.message){
					console.log(r.message)
					console.log(items.unit_of_measure)
					items.unit_of_measure=r.message
					cur_frm.refresh_fields()
				}
			}
		});
})

frappe.ui.form.on("Purchase Invoice Item","item_code" ,function(frm,cdt,cdn){
	if (cur_frm.doc.supplier=="")
	{
	frappe.throw(__("Please Enter Supplier Name"))	
	}
	items=locals[cdt][cdn]
	return frappe.call({
			method: "glosel.api.fetch_supplier_uom",
			args: {
				supplier: frm.doc.supplier,
				item:items.item_code
			},
			callback: function(r) {
				if(r.message){
					console.log(r.message)
					console.log(items.unit_of_measure)
					items.unit_of_measure=r.message
					cur_frm.refresh_fields()
				}
			}
		});
})

frappe.ui.form.on("Item","brand" ,function(frm){
	console.log("ffff",frm.doc.brand)
	frappe.call({
		method:"glosel.custom_py_methods.item_autoname",
		args:{
			"brand":frm.doc.brand
		},
		callback: function(r) {
				if(r.message){
					console.log(r.message)
					frm.doc.item_code=r.message
					cur_frm.refresh_fields()
				}
			}
		});
	})



// CustomSalesOrderController = erpnext.selling.SalesOrderController.extend({
// 	make_delivery_note:function(){
// 		console.log("in chcild")
// 	}
// })

// $.extend(cur_frm.cscript, new erpnext.selling.CustomSalesOrderController({frm: cur_frm}));




// cur_frm.cscript.create_salary_slip  = function(doc, cdt, cdn) {
// 	cur_frm.cscript.display_activity_log("");
// 	var callback = function(r, rt){
// 		if (r.message)
// 			cur_frm.cscript.display_activity_log(r.message);
// 	}
// 	return $c('runserverobj', args={'method':'glosel.custom_py_methods.create_sal_slip','docs':cur_frm.doc},callback);
	
// }
