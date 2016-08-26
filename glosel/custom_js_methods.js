// frappe.ui.form.on("Supplier Quotation Item","item_code" ,function(frm,cdt,cdn){
// 	if (cur_frm.doc.supplier=="")
// 	{
// 	frappe.throw(__("Please Enter Supplier Name"))	
// 	}
// 	items=locals[cdt][cdn]
// 	return frappe.call({
// 			method: "glosel.api.fetch_supplier_uom",
// 			args: {
// 				supplier: frm.doc.supplier,
// 				item:items.item_code
// 			},
// 			callback: function(r) {
// 				if(r.message){
// 					// console.log(r.message)
// 					// console.log(items.unit_of_measure)
// 					// items.unit_of_measure=r.message
// 					// items.uom=r.message
// 					console.log(items.uom)
// 					// cur_frm.refresh_fields()
// 					frappe.model.set_value(cdt, cdn, "uom", r.message);
// 					console.log("before refresh",items.uom)
// 					cur_frm.refresh_field("items")
// 					console.log("after Refresh",items.uom)
// 				}
// 			}
// 		});
// })

// frappe.ui.form.on("Purchase Order Item","item_code" ,function(frm,cdt,cdn){
// 	if (cur_frm.doc.supplier=="")
// 	{
// 	frappe.throw(__("Please Enter Supplier Name"))	
// 	}
// 	items=locals[cdt][cdn]
// 	return frappe.call({
// 			method: "glosel.api.fetch_supplier_uom",
// 			args: {
// 				supplier: frm.doc.supplier,
// 				item:items.item_code
// 			},
// 			callback: function(r) {
// 				if(r.message){
// 					// console.log(r.message)
// 					// console.log(items.unit_of_measure)
// 					// items.unit_of_measure=r.message
// 					// items.uom=r.message
// 					// console.log(items.uom)
// 					// cur_frm.refresh_fields()
// 					frappe.model.set_value(cdt, cdn, "uom", r.message);
// 					console.log("before refresh",items.uom)
// 					cur_frm.refresh_field("items")
// 					console.log("after Refresh",items.uom)

// 				}
// 			}
// 		});
// })

// frappe.ui.form.on("Purchase Receipt Item","item_code" ,function(frm,cdt,cdn){
// 	if (cur_frm.doc.supplier=="")
// 	{
// 	frappe.throw(__("Please Enter Supplier Name"))	
// 	}
// 	items=locals[cdt][cdn]
// 	return frappe.call({
// 			method: "glosel.api.fetch_supplier_uom",
// 			args: {
// 				supplier: frm.doc.supplier,
// 				item:items.item_code
// 			},
// 			callback: function(r) {
// 				if(r.message){
// 					console.log(r.message)
// 					console.log(items.unit_of_measure)
// 					// items.unit_of_measure=r.message
// 					items.uom=r.message
// 					console.log(items.uom)
// 					// cur_frm.refresh_fields()
// 				}
// 			}
// 		});
// })

// frappe.ui.form.on("Purchase Invoice Item","item_code" ,function(frm,cdt,cdn){
// 	if (cur_frm.doc.supplier=="")
// 	{
// 	frappe.throw(__("Please Enter Supplier Name"))	
// 	}
// 	items=locals[cdt][cdn]
// 	return frappe.call({
// 			method: "glosel.api.fetch_supplier_uom",
// 			args: {
// 				supplier: frm.doc.supplier,
// 				item:items.item_code
// 			},
// 			callback: function(r) {
// 				if(r.message){
// 					console.log(r.message)
// 					console.log(items.unit_of_measure)
// 					// items.unit_of_measure=r.message
// 					items.uom=r.message
// 					// cur_frm.refresh_fields()
// 				}
// 			}
// 		});
// })

// frappe.ui.form.on("Item","brand" ,function(frm){
// 	console.log("ffff",frm.doc.brand)
// 	frappe.call({
// 		method:"glosel.custom_py_methods.item_autoname",
// 		args:{
// 			"brand":frm.doc.brand
// 		},
// 		callback: function(r) {
// 				if(r.message){
// 					// console.log(r.message)
// 					frm.doc.item_code=r.message
// 					console.log(items.uom)
// 					// cur_frm.refresh_fields()
// 				}
// 			}
// 		});
// 	})



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
// frappe.ui.form.on("Delivery Note","onload" ,function(frm){
// 	items=cur_frm.doc.items
// 	if (cur_frm.doc.is_return==1)
// 	{
// 	return frappe.call({
// 			method: "glosel.api.fetch_supplier_uom",
// 			args: {
// 				return_against: frm.doc.return_against,
				
// 			},
// 			callback: function(r) {
// 				if(r.message){
// 					// console.log(r.message)
// 					// console.log(items.unit_of_measure)
// 					// items.unit_of_measure=r.message
// 					// items.uom=r.message
// 					console.log(items.uom)
// 					// cur_frm.refresh_fields()
// 					frappe.model.set_value(cdt, cdn, "uom", r.message);
// 					console.log("before refresh",items.uom)
// 					cur_frm.refresh_field("items")
// 					console.log("after Refresh",items.uom)
// 				}
// 			}
// 		});
// 	}
	
	
// })

cur_frm.cscript.on_update=function(doc)
{

		function_name()
	}

// custom_cakes_dialog: function () {
// 		var me = this;
// 		var dialog = new frappe.ui.Dialog({
// 			width: 1100,
// 			title: "Select <b>Custom Cake</b> Size",
// 			fields:[
// 				{fieldtype: 'HTML',
// 					fieldname:'item_images', label: __("Item Images")},
// 				{fieldtype: "Section Break", fieldname: "sb1"},
// 				{fieldtype : 'Int',
// 					fieldname:'age', label: __("Age")},
// 				{fieldtype: "Column Break", fieldname: "cb3"},
// 				{fieldtype: 'Section Break',
// 					fieldname:'sb01'},
// 				{fieldtype: 'Button', label: __("Add to Cart"), fieldname: "order_item"},
// 				{fieldtype: "Column Break", fieldname: "cb4"},
// 				{fieldtype: 'Button', label: __("Next"), fieldname: "next"}
// 			]
// 		});
// 		dialog.show();
// 		// body...
// }

	
function_name =function (argument) {
	 	var me = this;
		var dialog = new frappe.ui.Dialog({
			width: 1100,
			title: "Select <b>Custom Cake</b> Size",
			fields:[
				{fieldtype: 'HTML',
					fieldname:'item_images', label: __("Item Images")},
				{fieldtype: "Section Break", fieldname: "sb1"},
				{fieldtype : 'Int',
					fieldname:'age', label: __("Age")},
				{fieldtype: "Column Break", fieldname: "cb3"},
				{fieldtype: 'Section Break',
					fieldname:'sb01'},
				{fieldtype: 'Button', label: __("Add to Cart"), fieldname: "order_item"},
				{fieldtype: "Column Break", fieldname: "cb4"},
				{fieldtype: 'Button', label: __("Next"), fieldname: "next"}
			]
		});
		dialog.show();
}