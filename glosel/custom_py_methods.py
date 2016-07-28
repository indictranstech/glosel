import frappe
import json
import frappe.utils
from frappe import _
from frappe.model.naming import make_autoname
import frappe.defaults
# from erpnext.selling.doctype.customer.customer import get_customer_outstanding

@frappe.whitelist(allow_guest=True)
def get_customer_credit_limit_with_oustanding(so):
	sales_order=frappe.get_doc("Sales Order",so)
	cust=frappe.get_doc("Customer",sales_order.customer)
	credit_limit= cust.credit_limit 
	name=cust.name
	company=sales_order.company
	outstanding_amount = get_customer_outstanding(name, company)
	# print "Outstangiing Amount",outstanding_amount
	# print"outstanding is", get_customer_outstanding(name, company)
	# print "Credit Limit is",credit_limit
	available_amount=credit_limit-outstanding_amount
	# print "available_amount",available_amount
	if sales_order.grand_total>available_amount:
		# print "Outstanding"
		return 0
	else: 
		# print "No Outstanding"
		return 1 

@frappe.whitelist()
def create_sal_slip(doc):

	"""
		Creates salary slip for selected employees if already not created
	"""
	doc1=json.loads(doc)
	pp=frappe.get_doc("Process Payroll",doc1.get('name'))
	emp_list=pp.get_emp_list()
	# emp_list = []
	ss_list = []
	for emp in emp_list:
		employee=frappe.get_doc("Employee",emp[0])
		# if employee.esi_ip_number:
		# 	print "ESI IP",employee.esi_ip_number
	# 	if not frappe.db.sql("""select name from `tabSalary Slip`
	# 			where docstatus!= 2 and employee = %s and month = %s and fiscal_year = %s and company = %s
	# 			""", (emp[0], doc1.get('month'), doc1.get('fiscal_year'), doc1.get('company')):
	# 		ss = frappe.get_doc({
	# 			"doctype": "Salary Slip",
	# 			"fiscal_year": doc.fiscal_year,
	# 			"employee": emp[0],
	# 			"month": doc.month,
	# 			"company": doc.get("company"),
	# 			"esi_ip_number":employee.esi_ip_number,
	# 			"pan":employee.pan
	# 			# "epfo_pf_account_number":emp[0].epfo_pf_account_number,
	# 			# "esi_ip_number":emp[0].esi_ip_number,
	# 			# "pan":e[0].pan
	# 		})
	# 		# print "employee",emp[0].employee_name
	# 		ss.insert()
	# 		ss_list.append(ss.name)

	# return doc.create_log(ss_list)

def customer_validation(doc,method):
	roles=frappe.get_roles(frappe.session.user)
	if "Distributer" in roles:
		if doc.customer_group=="Distributer" or doc.customer_group=="Super Stockist":
			frappe.throw(_("You can not create a Distributor or Super Stockist"))


	if doc.customer_group=="Distributer":
		company_check=frappe.db.get_value("Company",{"company_name":doc.customer_name},"company_name")
		if not company_check:
			company=frappe.new_doc("Company")
			company.company_name=doc.customer_name
			company.abbr=doc.customer_name[0:5]
			company.default_currency="INR"
			company.save()

def delivery_note_submit(doc,method):
	customer=frappe.get_doc("Customer",doc.customer)
	if customer.customer_group=="Distributer":
		se=frappe.new_doc("Stock Entry")
		se.purpose="Material Receipt"
		se.posting_date=frappe.utils.nowdate()
		se.posting_time=frappe.utils.nowtime()
		se.company=customer.customer_name
		# se.from_warehouse="Finished Goods"+ " - " + customer.customer_name[5]
		# se.from_warehouse = "Stores - GIPL"
		for raw in doc.get("items"):
			se_items = se.append('items', {})
			se_items.item_code=raw.item_code
			se_items.qty=raw.qty
			se_items.uom=raw.stock_uom
			se_items.t_warehouse="Finished Goods" + " " + "-" + " " + doc.customer_name[0:5] 
			se_items.cost_center="Main" + " " + "-" + " " + doc.customer_name[0:5] 
			

		
		se.save()
		se.submit()

def employee_autoname(doc,method):
		# frappe.errprint("Inside autoname emp ")
		total=0
		company_code=str(frappe.db.get_value("Company",{"name":doc.company},"code"))
		employmement_code=doc.code
		number=make_autoname(company_code+str(employmement_code)+'.####')
		# temp_code=number.split()
		for i in number:
			j=1
			if j%2==0:
				total=total+int(i)*1
				j+=1
			else:
				total=total+int(i)*3
				j+=1
		sum_last_digit=total%10
		if sum_last_digit==0:
			check_digit=0
		else:
			check_digit=10-sum_last_digit
		doc.name=str(number)+str(check_digit)

@frappe.whitelist()
def item_autoname(brand):
	
	brand_code=str(frappe.db.get_value("Brand",{"name":brand},"code"))
	# doc.item_code = brand_code + '0001'
	item_code = make_autoname(brand_code + '.####')
	return item_code

def so_validate(doc,method):
	# print "Inside ------------------------"
	if doc.company!=frappe.defaults.get_defaults().get("company"):
		# print "Inside if "
		for raw in doc.get("items"):
			raw.warehouse="Finished Goods" + " " + "-" + " " + doc.company[0:5]
			# print raw.warehouse,"Arpit_____________________"
def employement_type_code_check(doc,method):
	code=frappe.db.get_value("Employment Type",{"code":doc.code},"code")
	if code==doc.code:
		frappe.throw(_("Employment Code already present ,please choose diffrent code"))



	









	

