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
		item=frappe.get_doc("Item",raw.item_code)
		item_code=raw.item_code
		item_group=item.item_group
		brand=item.brand
		scheme=frappe.db.sql("""select title from `tabScheme Management` where date(valid_from)<=%s and date(valid_upto)>=%s and brand=%s or item_code=%s or item_group=%s and company= %s or territory= %s order by CAST(priority as UNSIGNED) desc  limit 1""",(doc.transaction_date,doc.transaction_date,brand,item_code,item_group,company,company_territory),debug=True)
	print "Scheeeeeeeme",scheme
