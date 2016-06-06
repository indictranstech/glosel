import frappe
from erpnext.selling.doctype.customer.customer import get_customer_outstanding

def get_customer_credit_limit_with_oustanding(cusomer,company,so_amount):
	cust=frappe.get_doc("Customer",customer)
	name=cust.name
	credit_limit= cust.credit_limit 
	company=cust.company
	oustanding_amount=get_customer_outstanding(name,company)
	print "Outstangiing Amount",oustanding_amount
	available_amount=credit_limit-outstanding_amount
	if so_amount>available_amount:
		return 0
	else: 
		return 1 

