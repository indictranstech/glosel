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



CustomSalesOrderController = erpnext.selling.SalesOrderController.extend({
	make_delivery_note:function(){
		console.log("in chcild")
	}
})

$.extend(cur_frm.cscript, new erpnext.selling.CustomSalesOrderController({frm: cur_frm}));






