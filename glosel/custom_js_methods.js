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
frappe.ui.form.on("Delivery Note","onload" ,function(frm){
	items=cur_frm.doc.items
	if (cur_frm.doc.is_return==1)
	{
	return frappe.call({
			method: "glosel.api.fetch_supplier_uom",
			args: {
				return_against: frm.doc.return_against,
				
			},
			callback: function(r) {
				if(r.message){
					// console.log(r.message)
					// console.log(items.unit_of_measure)
					// items.unit_of_measure=r.message
					// items.uom=r.message
					console.log(items.uom)
					// cur_frm.refresh_fields()
					frappe.model.set_value(cdt, cdn, "uom", r.message);
					console.log("before refresh",items.uom)
					cur_frm.refresh_field("items")
					console.log("after Refresh",items.uom)
				}
			}
		});
	}	
})

cur_frm.cscript.onload = function(doc,cdt,cdn) {
	find_lat_lon(doc, 1);
}

cur_frm.cscript.validate = function(doc,cdt,cdn) {
	find_lat_lon(doc, 1);
}
cur_frm.cscript.refresh = function(doc,cdt,cdn) {
	find_lat_lon(doc, 1);
}

find_lat_lon = function(doc, count) {
	var full_address = post_code_address = ''
	if(doc.building_no)
		full_address += doc.building_no
	if(doc.building_name)
		full_address += "+"+doc.building_name+","
	if(doc.street_name)
		full_address += "+"+doc.street_name+","
	if(doc.area)
		full_address += "+"+doc.area+","
	
	full_address += "+"+doc.city+","+"+"+doc.country
	post_code_address += doc.city+","+"+"+doc.state+","+"+"+doc.country
	post_code = doc.post_code
	
	if(count <= 3 && count == 1){
		addr = full_address
	}
	else if(count <= 3 && count == 2){
		addr = post_code_address
	}
	else if(count <= 3 && count == 3){
		addr = post_code
	}
	else {
		frappe.throw("Please Check Address and Post Code")
	}
	addr = addr.split(' ').join('+')
	addr = addr.toLowerCase();
	$.ajax({
		async: false,
		cache: false,
		url: "http://nominatim.openstreetmap.org/search?q="+addr+"&format=json&addressdetails=1&limit=1&polygon_svg=1", 
		success: function(result){
			if(result[0]){
				cur_frm.doc.longitude = result[0].lon
				cur_frm.doc.latitude = result[0].lat
				refresh_field("longitude")
				refresh_field("latitude")
				render_map_view(result[0].lon, result[0].lat, result[0].display_name)
			}
			else{
				find_lat_lon(doc, count+1)
			}
		}
	});
}

render_map_view = function(lon, lat, name) {
	$("#mapid").remove();
	console.log("lt,ln,name",lon, lat, name)
	html = $(frappe.render_template("street_view"))
	$(cur_frm.fields_dict.street_view.wrapper).html(html);

	var mymap = L.map('mapid').setView([flt(lat),flt(lon)], 13);

	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
		maxZoom: 20,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(mymap);

	var marker = L.marker([flt(lat),flt(lon)]).addTo(mymap);
	marker.bindPopup("<b>"+name+"</b>").openPopup();

	/*var popup = L.popup();

	function onMapClick(e) {
	popup
	.setLatLng(e.latlng)
	.setContent("You clicked the map at " + e.latlng.toString())
	.openOn(mymap);
	}
	mymap.on('click', onMapClick);*/
}

/*country_calling_code = function(doc) {
	if(doc.phone && doc.country_code) {
		frappe.call({
			method: "glosel.custom_py_methods.generate_calling_code",
			args: {"phone": doc.phone, "code": doc.country_code},
			callback: function(r) {
				if(r.message)
					cur_frm.set_value("phone", r.message)
			}
		})
	}

}*/