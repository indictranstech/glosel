
import frappe
import frappe.defaults
from frappe import _
import json
def so_validate(doc,method):
	pass
	
	
def so_update(doc,method):
	pass

	
		
def so_before_submit(doc,method):
	pass
	
def so_submit(doc,method):
	pass

def distributer_outstanding_add(doc,method):
	print """called on dn submit"""
	if doc.is_return==0:
		flag=None
		# print "Inside distributer_outstanding"
		if doc.company !=frappe.defaults.get_defaults().get("company"):
		# if doc.company !="Glosel India PVT LTD":
			for raw in doc.get("items"):
				if raw.is_free_item==1:
					item_doc=frappe.get_doc("Item",raw.item_code)
					for raw1 in item_doc.get("distributer_outstanding"):
						if raw1.company==doc.company:
							raw1.qty=raw1.qty+raw.qty
							flag=1		
				 	if not flag :	
						do = item_doc.append('distributer_outstanding', {})
						do.company=doc.company
						do.qty=raw.qty
						# do.save()
					item_doc.save()
	else:
		if doc.company!=frappe.defaults.get_defaults().get("company"):
		# if doc.company !="Glosel India PVT LTD":
			for raw in doc.get("items"):
				if raw.is_free_item==1:
					item_doc=frappe.get_doc("Item",raw.item_code)
					for raw1 in item_doc.get("distributer_outstanding"):
						if raw1.company==doc.company:
							raw1.qty=raw1.qty+raw.qty
							item_doc.save()
									
def dn_submit(doc,method):
	create_customerwise_item_on_dn_submit(doc,method)
	if doc.is_return==0:
		print "dn -------------------------------------"
		customer=frappe.get_doc("Customer",doc.customer)
		customer_company=doc.company
		if customer_company!=frappe.defaults.get_defaults().get("company"):
			customer_company_name=frappe.db.get_value("Customer",{"customer_name":customer_company},"name")
			company=frappe.get_doc("Customer",customer_company_name)
			company_territory=company.territory 
		else:
			company=frappe.defaults.get_defaults().get("company")
			glosel_object=frappe.get_doc("Company",frappe.defaults.get_defaults().get("company"))
			company_territory=customer.territory

		for raw in doc.get("items"):
			if raw.is_free_item==0 and customer.customer_group!="Distributer":
				item=frappe.get_doc("Item",raw.item_code)
				item_code=raw.item_code
				item_group=item.item_group
				brand=item.brand
				so_customer=doc.customer
				customer_group=doc.customer_group
				scheme_title=frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s) 
	 		 order by CAST(priority as UNSIGNED) desc""",(doc.posting_date,doc.posting_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)
				# gives all the schemes applicable on current  item,brand and item group irrespective of amount and quantity
				scheme_list=[]
				for i in scheme_title:
					if i :
						scheme_name = ""
						scheme_name=i.get("title")
						# scheme_list.append(scheme_name)
						# frappe.errprint(scheme_name)
						scheme_obj=frappe.get_doc("Scheme Management",scheme_name)
						if scheme_obj.apply_on=="Item Group" and scheme_obj.scheme_on=="Quantity":
							quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and item_group=%s""",(doc.customer,scheme_obj.item_group))

						elif scheme_obj.apply_on=="Item Code" and scheme_obj.scheme_on=="Quantity":
							# main_object_name=scheme_obj.item_code
							quantity=quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and item_code=%s""",(doc.customer,scheme_obj.item_code))
						elif scheme_obj.apply_on=="Brand" and scheme_obj.scheme_on=="Quantity": 
							# main_object_name=scheme_obj.brand
							quantity=quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and brand=%s""",(doc.customer,scheme_obj.brand))
						if quantity>=scheme_obj.minimum_quantity and quantity>=scheme_obj.quantity:
							scheme_list.append(scheme_name)

				# main_object_criteria=scheme_obj.apply_on
				# for scheme_raw in scheme_obj.get("freebie_items"):
				# 	free_object_criteria=scheme_raw.apply_on

def dn_update(doc,method):
	pass
	

def dn_return_submit(doc,method):
	print "on dn return code -------------------------------------"
	# frappe.errprint("Inside DN return update")
	if doc.is_return==1:
		depend_doc=frappe.get_doc("Delivery Note",doc.return_against)
		for i in range(len(doc.items)):
			if (doc.items[i].item_code==depend_doc.items[i].item_code) and (doc.items[i].rate==depend_doc.items[i].rate) and (not doc.items[i].is_free_item) and (depend_doc.items[i].qty>abs(doc.items[i].qty)):
				scheme_name=doc.items[i].scheme
				scheme=frappe.get_doc("Scheme Management",scheme_name)
				# actual quantity of original item
				actual_item_qty=doc.items[i].qty+depend_doc.items[i].qty
				for raw1 in doc.get("items"):
					if raw1.scheme==scheme_name and raw1.free_with==doc.items[i].item_code:
						# free item qty in dn return
						this_item_qty=raw1.qty
						# populating free items in the scheme 
						for freebie in scheme.get("freebie_items"):
							item_code=freebie.item_code
							# qty=freebie.quantity
							# scheme_item_dict={"item_code":item_code,"qty":qty}
							if item_code==raw1.item_code:
								# free item quantity specified in scheme master
								free_item_qty=freebie.quantity
								min_qty_actual_item=scheme.minimum_quantity
								# modified  quantity of free itemafter calculations
								new_qty_free_item=(actual_item_qty*free_item_qty)/min_qty_actual_item
								modulas=new_qty_free_item%free_item_qty
								final_new_qty_free_item=new_qty_free_item-modulas

								# actual quntity to be displayed
								raw1.qty = int(this_item_qty+final_new_qty_free_item)

								# frappe.errprint(raw1.qty)
def find_divisible_number(qty,sc_min_qty):
	print "on  find_divisible_number -------------------------------------"
	for i in range(qty,sc_min_qty-1,-1):
		if i%sc_min_qty==0:
			return i

def dn_on_cancel(doc,method):
	print "on  cancel -------------------------------------"
	if doc.company!=frappe.defaults.get_defaults().get("company") and doc.is_return==0:
		# if doc.company !="Glosel India PVT LTD":
		for raw in doc.get("items"):
			if raw.is_free_item==1:
				item_doc=frappe.get_doc("Item",raw.item_code)
				for raw1 in item_doc.get("distributer_outstanding"):
					if raw1.company==doc.company:
						raw1.qty=raw1.qty-raw.qty
						item_doc.save()


def dn_validate(doc,method):
	add_free_item(doc,method)
	# doc.total_price = 99
	total = 0
	total_free_qty = 0
	for raw in doc.get("items"):
# frappe.db.get_value("Company",doc.company,"default_expense_account")
		if raw.free_item_of_scheme:
			price_list_rate = frappe.db.get_value("Item Price",{"item_code": raw.item_code, "price_list": doc.selling_price_list}, "price_list_rate")
			total_free_qty = total_free_qty + raw.qty
			total = total+(price_list_rate*raw.qty)
	doc.total_price = total
	doc.total_qty_of_free_item = total_free_qty

	# frappe.msgprint("Total Price for free item is updated")
	# pass
	# frappe.msgprint("In dn validate")
	# add_free_item(doc,method)

	# doc.schemes=[]
	# create_customerwise_item_on_dn_submit(doc,method)
	# pass

	# dl = frappe.db.sql("""selectget_schemes name,title,apply_on, valid_from, valid_upto,scheme_type from `tabScheme Management` where active=1 and valid_upto > now();""",as_dict=1, debug=1)

	# # for i in range(len(doc.items)):
	# # 	pass
	# dn_items = []
	# for raw in doc.get("items"):
	# 	dn_items.append(raw.item_code)
	# 	print "\n\nItem COde",raw.item_code
	# print "full list",dn_items
	# print "fisrt item",dn_items[0]
	# item_code_for_check = dn_items[0]
	# dn_customer = doc.customer

	# scheme_title= frappe.db.sql("""select title from `tabScheme Management` where active=1 and valid_upto > now() and item_code=%s""",(item_code_for_check),as_dict=1)
	# print "scheme_title",scheme_title
	# # frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s) 
	# #  		 order by CAST(priority as UNSIGNED) desc""",(doc.posting_date,doc.posting_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)
	# # gives all the schemes applicable on current  item,brand and item group irrespective of amount and quantity
	# scheme_list=[]
	# for i in scheme_title:
	# 	scheme_list.append(i["title"])
	# print "scheme_list",scheme_list

	# scheme_obj = frappe.get_doc("Scheme Management",scheme_list[0])
	# print "\napply",scheme_obj.apply_on

	# available_scheme_list = []
	# if scheme_obj.apply_on=="Item Code" and scheme_obj.scheme_on=="Quantity":
	# 	# main_object_name=scheme_obj.item_code
	# 	effective_qty=frappe.db.sql("""select sum(effective_qty) as effective_qty from `tabCustomerwise Item` 
	# 		where customer=%s and item_code=%s""",(dn_customer,item_code_for_check),as_dict=1)
	# 	print "effective_qty",effective_qty[0]["effective_qty"]
	# 	effective_qty_check = effective_qty[0]["effective_qty"]

	# 	for i in scheme_list:
	# 		scheme_obj = frappe.get_doc("Scheme Management",i)
	# 		#if scheme on qty
	# 		if scheme_obj.scheme_on=="Quantity":
	# 			if effective_qty_check>=scheme_obj.minimum_quantity and effective_qty_check>=scheme_obj.quantity:
	# 				available_scheme_list.append(scheme_obj.title)
	# 		elif scheme_obj.scheme_on=="Price":
	# 			#check for price validations like on 50k give 5k free
	# 			pass

	# 	print "\nScheme Available",available_scheme_list
	# 	for raw in doc.get("items"):
	# 		if raw.is_free_item==0 and customer.customer_group!="Distributer":
	# 			item=frappe.get_doc("Item",raw.item_code)
	# 			item_code=raw.item_code
	# 			item_group=item.item_group
	# 			brand=item.brand
	# 			so_customer=doc.customer
	# 			customer_group=doc.customer_group
	# 			scheme_title=frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s) 
	#  		 order by CAST(priority as UNSIGNED) desc""",(doc.posting_date,doc.posting_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)
	# 			# gives all the schemes applicable on current  item,brand and item group irrespective of amount and quantity
	# 			scheme_list=[]

	# 			for i in scheme_title:
	# 				if i :
	# 					scheme_name=i.get("title")
	# 					# scheme_list.append(scheme_name)
	# 					# frappe.errprint(scheme_name)
	# 			scheme_obj=frappe.get_doc("Scheme Management",scheme_name)
	# 			if scheme_obj.apply_on=="Item Group" and scheme_on=="Quantity":
	# 				quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and item_group=%s""",(doc.customer,scheme_obj.item_group))

	# 			elif scheme_obj.apply_on=="Item Code" and scheme_on=="Quantity":
	# 				# main_object_name=scheme_obj.item_code
	# 				quantity=quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and item_code=%s""",(doc.customer,scheme_obj.item_code))
	# 			elif scheme_obj.apply_on=="Brand" and scheme_on=="Quantity": 
	# 				# main_object_name=scheme_obj.brand
	# 				quantity=quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and brand=%s""",(doc.customer,scheme_obj.brand))
	# 			if quantity>=scheme_obj.minimum_quantity and quantity>=scheme_obj.quantity:
	# 				scheme_list.append(scheme_name)


@frappe.whitelist()
def get_schemes(doc):
	#get available scheme
	# print "In dn get_schemes"
	# doc.schemes=[]
	# create_customerwise_item_on_dn_submit(doc,method)

	dl = frappe.db.sql("""select name,title,apply_on, valid_from, valid_upto,scheme_type from `tabScheme Management` where active=1 and valid_upto > now();""",as_dict=1, debug=1)

	# for i in range(len(doc.items)):
	# 	pass
	doc = json.loads(doc)
	dn_items = []
	for raw in doc.get("items"):
		print "\n\n\nraw",raw["item_code"]
		dn_items.append(raw["item_code"])
		print "\n\nItem COde",raw["item_code"]
	# print "full list",dn_items
	# print "fisrt item",dn_items[0]
	dn_customer = doc["customer"]

	# item_code_for_check = dn_items

	available_scheme_list = []

# for raw in doc.get("items"):
	print "\n\customer_group",doc.get("customer_group")
	if doc.get("customer_group") == "Distributer":
		company = doc.get("company")
		print "Distributer Scheme"
		scheme_title= frappe.db.sql("""select title from `tabScheme Management` where active=1 and valid_upto > now() and item_code=%s and scheme_depends_upon='Company' and company=%s""",(raw["item_code"],company),as_dict=1)
	else:
		print "non distributor"
		scheme_title= frappe.db.sql("""select title from `tabScheme Management` where active=1 and valid_upto > now() and item_code=%s and scheme_depends_upon='ALL'""",(raw["item_code"]),as_dict=1)
	# item_obj = frappe.get_doc("Item",raw["item_code"])
	# scheme_title_group= frappe.db.sql("""select title from `tabScheme Management` where active=1 and valid_upto > now() and item_group=%s""",(item_obj.item_group),as_dict=1)
	scheme_title_group= frappe.db.sql("""select title from `tabScheme Management` where active=1 and valid_upto > now() and apply_on='Item Group'""",as_dict=1)

	print "scheme_title",scheme_title
	# frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s) 
	#  		 order by CAST(priority as UNSIGNED) desc""",(doc.posting_date,doc.posting_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)
	# gives all the schemes applicable on current  item,brand and item group irrespective of amount and quantity
	scheme_list=[]
	scheme_list_for_group=[]
	for i in scheme_title_group:
		scheme_list_for_group.append(i["title"])
	for i in scheme_title:
		scheme_list.append(i["title"])
	# print "\n\nscheme_listttttt",scheme_list

	# print "\n\schemelist for Item Group",scheme_list

	for i in scheme_list:
		if i:
			scheme_obj = frappe.get_doc("Scheme Management",i)
			# print "\napply",scheme_obj.apply_on
			# print "\n item code in dn",raw["item_code"]


		if scheme_obj.apply_on=="Item Code" and scheme_obj.scheme_on=="Quantity":
			# main_object_name=scheme_obj.item_code
			effective_qty=frappe.db.sql("""select sum(effective_qty) as effective_qty from `tabCustomerwise Item` 
				where customer=%s and item_code=%s""",(dn_customer,raw["item_code"]),as_dict=1)
			print "effective_qty",effective_qty[0]["effective_qty"]
			effective_qty_check = effective_qty[0]["effective_qty"]

			# for i in scheme_list:
			scheme_obj = frappe.get_doc("Scheme Management",i)
			#if scheme on qty
			if scheme_obj.scheme_on=="Quantity":
				if effective_qty_check>=float(scheme_obj.minimum_quantity) and effective_qty_check>=float(scheme_obj.quantity):
					print "in add schm"
					available_scheme_list.append(scheme_obj.title)
				# elif scheme_obj.scheme_on=="Price":
				# 	#check for price validations like on 50k give 5k free
				# 	pass

			# print "\nScheme Available list initial",available_scheme_list

		#Check Item Price Validation
		if scheme_obj.apply_on=="Item Code" and scheme_obj.scheme_on=="Price":
			effective_amount_check=frappe.db.sql("""select sum(effective_amount) as effective_amount from `tabCustomerwise Item` 
				where customer=%s and item_code=%s""",(dn_customer,raw["item_code"]),as_dict=1)
			# print "\neffective_amount",effective_amount_check
			if effective_amount_check>=scheme_obj.amount:
					available_scheme_list.append(scheme_obj.title)
	
	# print "scheme_list_for_group--------",scheme_list_for_group
	for i in scheme_list_for_group:
		if i:
			scheme_obj = frappe.get_doc("Scheme Management",i)

		#need to check item group
		if scheme_obj.apply_on=="Item Group" and scheme_obj.scheme_on=="Quantity":
			effective_qty_check=frappe.db.sql("""select sum(effective_qty) as effective_qty from 
				`tabCustomerwise Item`  where customer=%s  group by item_group having item_group=%s""",(dn_customer,scheme_obj.item_group),as_dict=1,debug=1)
			if effective_qty_check:
				effective_qty_check = effective_qty_check[0]["effective_qty"]
				if effective_qty_check>=scheme_obj.minimum_quantity and effective_qty_check>=scheme_obj.quantity:
						available_scheme_list.append(scheme_obj.title)
		
		if scheme_obj.apply_on=="Item Group" and scheme_obj.scheme_on=="Price":
			effective_amount_check=frappe.db.sql("""select sum(effective_amount) as effective_amount from 
				`tabCustomerwise Item`  where customer=%s  group by item_group having item_group=%s""",(dn_customer,scheme_obj.item_group),as_dict=1,debug=1)
			if effective_amount_check:
				effective_amount_check = effective_amount_check[0]["effective_amount"]
				if effective_amount_check>=scheme_obj.amount:
						available_scheme_list.append(scheme_obj.title)

	print "available_scheme_list",available_scheme_list
	id_list = tuple([x.encode('UTF8') for x in available_scheme_list if x])	
	#remove , at the end
	cond = ""
	if len(id_list) == 1:
		cond ="where title = '{0}' ".format(id_list[0]) 
	elif len(id_list) > 1:	
		cond = "where title in {0} ".format(id_list)
	elif len(id_list)==0:
		cond ="where title = '{0}' ".format("Dummy") 

	dl = frappe.db.sql("""select name,title,apply_on, valid_from, valid_upto,scheme_type from `tabScheme Management` {0}""".format(cond),as_dict=1, debug=1)
	print "title",cond
	print "\n\ndl",dl
	# dl = frappe.db.sql("""select name,title,apply_on, valid_from, valid_upto,scheme_type from `tabScheme Management` where active=1 and valid_upto > now();""",as_dict=1, debug=1)
	# frappe.msgprint(dl)
	return dl

def dn_before_submit(doc,method):
	add_free_item(doc,method)

def po_before_submit(doc,method):
	if doc.is_claim:
		add_free_item_in_po(doc,method)
		add_free_item_in_so_from_po(doc,method)


# def po_before_submit_create_so(doc,method):
# 	# create_customerwise_item_on_dn_submit(doc,method)
# 	add_free_item_in_so_from_po(doc,method)

def add_free_item_in_so_from_po(doc,method):
	frappe.msgprint("in add add_free_item_in_po")
	so_doc = frappe.new_doc("Sales Order")
	so_doc.customer = doc.company
	so_doc.delivery_date = frappe.utils.get_datetime()
	default_expense_account=frappe.db.get_value("Company",doc.company,"default_expense_account")
	cost_center=frappe.db.get_value("Company",doc.company,"cost_center")
	default_company=frappe.defaults.get_defaults().get("company")

	for raw in doc.get("items"):
		item = frappe.get_doc("Item",raw.item_code)
		nl = so_doc.append('items', {})
		nl.item_code = raw.item_code
		nl.item_name = item.item_name
		nl.description = item.description
		nl.stock_uom = item.stock_uom
		nl.warehouse = item.default_warehouse
		nl.expense_account = default_expense_account
		nl.cost_center = cost_center
		nl.qty=raw.qty
		nl.rate=0
		nl.amount=0
		nl.price_list_rate=0

	so_doc.save()

def add_free_item_in_po(doc,method):
	default_expense_account=frappe.db.get_value("Company",doc.company,"default_expense_account")
	cost_center=frappe.db.get_value("Company",doc.company,"cost_center")
	for raw in doc.get("claim_available"):
		if raw.selected_item:
			item = frappe.get_doc("Item",raw.selected_item)
		elif raw.item_code:
			item = frappe.get_doc("Item",raw.item_code)
		nl = doc.append('items', {})

		dn_item = frappe.get_doc("Delivery Note Item",raw.delivery_note_item)
		claim_for_qty = raw.qty*(dn_item.claim_for_qty/dn_item.qty)
		updated_claimed_qty_by_distributor = dn_item.claimed_qty_by_distributor+claim_for_qty 
		print "\nupdated_claimed_qty_by_distributor",updated_claimed_qty_by_distributor
		print "\ndn_item.claimed_qty_by_distributor",dn_item.claimed_qty_by_distributor
		if updated_claimed_qty_by_distributor < dn_item.claimed_qty_by_distributor:
			frappe.throw("You have allready claimed for this scheme and customer")
		
		nl.claim_for_qty = claim_for_qty
		frappe.db.set_value("Delivery Note Item", raw.delivery_note_item, "claimed_qty_by_distributor",updated_claimed_qty_by_distributor)
		nl.item_code = raw.item_code
		nl.item_name = item.item_name
		nl.description = item.description
		nl.stock_uom = item.stock_uom
		nl.warehouse = item.default_warehouse
		nl.expense_account = default_expense_account
		nl.cost_center = cost_center
		nl.delivery_note = raw.delivery_note
		nl.delivery_note_item = raw.delivery_note_item
		nl.scheme_name = raw.scheme_name
		nl.schedule_date = frappe.utils.get_datetime()
		nl.conversion_factor = 1
		nl.qty = raw.qty
		nl.rate = 0
		nl.base_rate = 0
		nl.amount = 0
		nl.base_amount = 0

def add_free_item(doc,method):
	#add item in DN
	dn_items = []
	default_expense_account=frappe.db.get_value("Company",doc.company,"default_expense_account")
	cost_center=frappe.db.get_value("Company",doc.company,"cost_center")
	frappe.msgprint("in add_free_item")
	for raw in doc.get("schemes_selected"):
		item = frappe.get_doc("Item",raw.item_code)
		dn_items.append(raw.item_code)
		nl = doc.append('items', {})
		nl.item_code = raw.item_code
		nl.item_name = item.item_name
		nl.description = item.description
		nl.stock_uom = item.stock_uom
		nl.warehouse = item.default_warehouse
		nl.expense_account = default_expense_account
		nl.cost_center = cost_center
		nl.qty = raw.qty
		nl.free_item_of_scheme = raw.scheme_name
		scheme = frappe.get_doc("Scheme Management",raw.scheme_name)
		nl.claim_for_qty = raw.qty*scheme.quantity

		#update claim details in CWI
		cwi = frappe.db.get_values("Customerwise Item",{"customer":doc.get("customer")},["qty","name"],as_dict=1)
		
		# print "\nccwi",cwi
		print "raw.qty",raw.qty
		# frappe.throw("Over Claim for item {0}".format(raw.item_code))

		qty_calculation = raw.qty
		for i in cwi:
			print "cwi",i
			if qty_calculation >0:	
				scm_doc = frappe.get_doc("Customerwise Item",i.name)
				print "in qty_calculation",qty_calculation
				if qty_calculation <= scm_doc.effective_qty:
					print "first"
					a = scm_doc.effective_qty
					scm_doc.effective_qty = scm_doc.effective_qty - a
					scm_doc.claim_for_qty = scm_doc.claim_for_qty + a
					print "ef qty",scm_doc.effective_qty
					print "qty_calculation",qty_calculation
					scm_doc.save()
				if qty_calculation > scm_doc.effective_qty:
					a = float(scm_doc.effective_qty)
					scm_doc = frappe.get_doc("Customerwise Item",i.name)
					print scm_doc.effective_qty
					print "for qty",scm_doc.qty
					print "scm_doc.effective_qty",float(scm_doc.effective_qty)
					print "a",a
					scm_doc.effective_qty = scm_doc.effective_qty - a
					scm_doc.claim_for_qty = scm_doc.claim_for_qty + a
					print "Value of a",a					
					scm_doc.save()
					qty_calculation = qty_calculation - a
					print " qty cal",qty_calculation					
					# break
		if qty_calculation>0:
			print "qty_calculationqty_calculation",qty_calculation
			frappe.throw("Over Claim for item {0}".format(raw.item_code))
				# break
		#add claim for price
		# print scheme.amount/
		print "claim_for_qty",raw.qty*scheme.quantity
	# frappe.msgprint("dn_before_submit")


def create_customerwise_item_on_dn_submit(doc,method):
	if doc.is_return!=1:
		for raw in doc.get("items"):
			if not raw.free_item_of_scheme:
				cwi=frappe.new_doc("Customerwise Item")
				cwi.customer=doc.customer
				cwi.brand=raw.brand
				cwi.item_code=raw.item_code
				cwi.item_group=raw.item_group
				cwi.qty=raw.qty
				cwi.effective_qty=raw.qty
				cwi.amount=raw.amount
				cwi.effective_amount=raw.amount
				cwi.date=doc.posting_date
				cwi.delivery_note=doc.name
				cwi.company = doc.company
				cwi.save()
			if raw.free_item_of_scheme:
				pass

@frappe.whitelist()
def change_item_in_po(doc,scheme_name):
	# frappe.msgprint("hi")
	apply_on=frappe.db.get_value("Scheme Management",{"name":scheme_name},"apply_on")

	print "\n\n\nhiiiiiiiiiii"
	print apply_on
	if apply_on=="Brand":
		dl = frappe.db.sql("""select brand from `tabScheme Management Item` where parent='{0}' and apply_on='Brand' and brand IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)
		# dl_item_price = frappe.db.sql("""select sum(price) as total_price from `tabScheme Management Item` where parent='{0}' and apply_on='Brand' and brand IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)
		# print "dl_item_price",dl_item_price

		brand_list = ""
		for k in dl:
			brand_list=brand_list+"'"+k['brand']+"'"+","
			# print k['brand']
		brand_list = brand_list[:-1]
		dl_item = frappe.db.sql("""select item_code,item_name,manufacturer_part_no from `tabItem` where brand in ({0})""".format(brand_list),as_dict=1, debug=1)
		# print "dl_item",dl_item
		# dl_item.append(dl_item_price[0])
		print dl_item
		return dl_item

	if apply_on=="Item Group":
		print "scheme for group"
		dl = frappe.db.sql("""select item_group,price from `tabScheme Management Item` where parent='{0}' and apply_on='Item Group' and item_group IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)
		# dl_item_price = frappe.db.sql("""select sum(price) as total_price from `tabScheme Management Item` where parent='{0}' and apply_on='Item Group' and item_group IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)

		# print dl_item_price
		item_group_list = ""
		for k in dl:
			item_group_list=item_group_list+"'"+k['item_group']+"'"+","
			# print k['item_group']
		item_group_list = item_group_list[:-1]
		# print "item_group_list",item_group_list
		dl_item = frappe.db.sql("""select item_code, item_name,manufacturer_part_no from `tabItem` where item_group in ({0})""".format(item_group_list),as_dict=1, debug=1)
		print "dl_item*****************************",dl_item
		# dl_item.append(dl_item_price[0])
		print "dl_item*****************************",dl_item
		return dl_item

@frappe.whitelist()
def get_free_item_by_brand(doc,apply_on,scheme_name):
	# frappe.msgprint("hi")
	print "\n\n\nhiiiiiiiiiii"
	if apply_on=="Brand":
		dl = frappe.db.sql("""select brand from `tabScheme Management Item` where parent='{0}' and apply_on='Brand' and brand IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)
		dl_item_price = frappe.db.sql("""select sum(price) as total_price from `tabScheme Management Item` where parent='{0}' and apply_on='Brand' and brand IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)
		print "dl_item_price",dl_item_price

		brand_list = ""
		for k in dl:
			brand_list=brand_list+"'"+k['brand']+"'"+","
			# print k['brand']
		brand_list = brand_list[:-1]
		dl_item = frappe.db.sql("""select item_code,item_name,manufacturer_part_no from `tabItem` where brand in ({0})""".format(brand_list),as_dict=1, debug=1)
		# print "dl_item",dl_item
		dl_item.append(dl_item_price[0])
		return dl_item
	if apply_on=="Item Code":
		dl = frappe.db.sql("""select smi.item_code,i.item_code,i.manufacturer_part_no from `tabScheme Management Item` as smi, tabItem as i 
			where smi.parent='{0}' and smi.apply_on='Item Code' and smi.item_code=i.item_code and smi.item_code IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)

		# print "\n",dl
		doc = json.loads(doc)
		customer = doc['customer']
		print "hi"
		effective_qty_per_item = []
		for i in dl:
			print i["item_code"]
			dli = frappe.db.sql("""select sum(effective_qty) as effective_qty from `tabCustomerwise Item` where 
				 customer = '{2}' group by item_code having item_code = '{1}'""".format(scheme_name,i["item_code"],customer),as_dict=1, debug=1)
			effective_qty_per_item.append(dli[0])
		
		# (29-22%3)/3
		scm_doc=frappe.get_doc("Scheme Management",scheme_name)
		for i in range(len(dl)):
			free_qty= frappe.db.sql("""select quantity from `tabScheme Management Item` where parent='{0}' and item_code='{1}'""".format(scheme_name,dl[i]['item_code']),as_dict=1,debug=1)
			print "ed",effective_qty_per_item[i]['effective_qty'],"b",scm_doc.quantity,"c",free_qty[0]['quantity']
			if scm_doc.quantity>0:
				a=effective_qty_per_item[i]['effective_qty']/(float(scm_doc.quantity)/free_qty[0]['quantity'])
				effective_qty_per_item[i]['effective_qty'] = a
			else:
				effective_qty_per_item[i]['effective_qty'] = 0
		for i in range(len(dl)):
		     dl[i]['effective_qty'] = effective_qty_per_item[i]['effective_qty']

		# print "updated",dli
		return dl
		#{"dict1":asdas,"dict":asdas}

	if apply_on=="Item Group":
		print "scheme for group"
		dl = frappe.db.sql("""select item_group,price from `tabScheme Management Item` where parent='{0}' and apply_on='Item Group' and item_group IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)
		dl_item_price = frappe.db.sql("""select sum(price) as total_price from `tabScheme Management Item` where parent='{0}' and apply_on='Item Group' and item_group IS NOT NULL""".format(scheme_name),as_dict=1, debug=1)

		print dl_item_price
		item_group_list = ""
		for k in dl:
			item_group_list=item_group_list+"'"+k['item_group']+"'"+","
			# print k['item_group']
		item_group_list = item_group_list[:-1]
		# print "item_group_list",item_group_list
		dl_item = frappe.db.sql("""select item_code, item_name,manufacturer_part_no from `tabItem` where item_group in ({0})""".format(item_group_list),as_dict=1, debug=1)
		print "dl_item*****************************",dl_item
		dl_item.append(dl_item_price[0])
		print "dl_item*****************************",dl_item
		return dl_item

@frappe.whitelist()
def get_claim_details(doc):
	frappe.msgprint("claim details")
	doc = json.loads(doc)
	print "\n\n\ncompany",doc["name"]
	dl = frappe.db.sql("""select dni.name as dni, dn.name as delivery_note, dn.customer,dni.item_code,dni.qty,dni.claim_for_qty,dni.free_item_of_scheme as scheme_name,
		 sm.apply_on,sm.scheme_type from `tabDelivery Note Item` as dni, `tabDelivery Note` dn, `tabScheme Management` sm where dn.name=dni.parent 
		 and dni.free_item_of_scheme=sm.name and dni.claim_for_qty!=0 and dni.claimed_qty_by_distributor<dni.claim_for_qty and dn.company='{0}'""".format(doc["company"]),as_dict=1, debug=1)
	print "\n\ndl_for_claim",dl

	# po_items = []
	for raw in dl:
		print "\n\n\nrassw",raw.item_code

	return dl
		# dn_items.append(raw["item_code"])
