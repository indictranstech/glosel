import frappe
def so_submit(doc,method):
	# end customer object
	customer=frappe.get_doc("Customer",doc.customer)
	# gives distributor name who is actually a company to end customer
	customer_company=customer.company
	if customer_company!="Glosel India PVT LTD":
	# gives distributer object which is actually a company on SO to find the terretory of distributor
		company=frappe.get_doc("Customer",customer_company)
		company_territory=company.territory 
	else:
		company="Glosel India PVT LTD"
		glosel_object=frappe.get_doc("Company","Glosel India PVT LTD")
		company_territory="India"

	
	for raw in doc.get("items"):
		if raw.rate!=0 and customer.customer_group!="Distributer":
			item=frappe.get_doc("Item",raw.item_code)
			item_code=raw.item_code
			item_group=item.item_group
			brand=item.brand
			qty=raw.qty
			scheme_title=frappe.db.sql("""select title from `tabScheme Management` where  (active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s) and (brand=%s or item_code=%s or item_group=%s and company=%s or territory=%s)  order by CAST(priority as UNSIGNED) desc  limit 1""",(doc.transaction_date,doc.transaction_date,brand,item_code,item_group,company,company_territory),as_dict=True)
			# frappe.errprint(scheme_title)datta mandir road wakad
			# scheme_name=scheme_title[0]["title"]
			for i in scheme_title:
				if i :
					scheme_name=i.get("title")
					scheme=frappe.get_doc("Scheme Management",scheme_name)
					# frappe.errprint(scheme)
					if int(qty)>=int(scheme.minimum_quantity):
						for scheme_raw in scheme.get("freebie_items"):
							free_items = doc.append('items', {})
							free_items.is_free_item=1
							free_items.item_code=scheme_raw.item_code
							free_items.item_name=scheme_raw.item_code
							# Source item name
							free_items.free_with=raw.item_code
							free_items.scheme=scheme_name
							if scheme.brand:
								name=scheme.brand
							elif scheme.item_code:
								name=scheme.item_code
							elif scheme.item_group:
								name=scheme.item_group
							free_items.description="Free with {0} {1}".format(scheme.minimum_quantity,name)
							# free_items.qty=scheme_raw.quantity
							real_quantity=int((qty*scheme_raw.quantity)/scheme.minimum_quantity)
							# print "Real Quantity is",real_quantity

							modulas=real_quantity%scheme.minimum_quantity
							if real_quantity<scheme.minimum_quantity:
								modulas=0
							# print "Modulas is",modulas
							free_items.qty=real_quantity-(modulas)
							free_items.rate=0
							free_items.save()

def dn_submit(doc,method):
	for raw in doc.get("items"):
		if raw.is_free_item==1:
			sml=frappe.new_doc("Scheme Management Log")
			sml.date=doc.posting_date
			sml.distributer=doc.company
			sml.dn=doc.name
			# sml.item=raw.item_code







		












		