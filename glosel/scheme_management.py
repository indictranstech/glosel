import frappe
def so_submit(doc,method):
	# end customer object
	customer=frappe.get_doc("Customer",doc.customer)
	# gives distributor name who is actually a company to end customer
	customer_company=customer.company
	# gives distributer object which is actually a company on SO to find the terretory of distributor
	company=frappe.get_doc("Customer",customer_company)
	company_territory=company.territory 
	
