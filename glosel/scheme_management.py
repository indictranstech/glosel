
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
						scheme_name=i.get("title")
						# scheme_list.append(scheme_name)
						# frappe.errprint(scheme_name)
				scheme_obj=frappe.get_doc("Scheme Management",scheme_name)
				if scheme_obj.apply_on=="Item Group" and scheme_on=="Quantity":
					quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and item_group=%s""",(doc.customer,scheme_obj.item_group))

				elif scheme_obj.apply_on=="Item Code" and scheme_on=="Quantity":
					# main_object_name=scheme_obj.item_code
					quantity=quantity=frappe.db.sql("""select sum(effective_qty) from `tabCustomerwise Item` where customer=%s and item_code=%s""",(doc.customer,scheme_obj.item_code))
				elif scheme_obj.apply_on=="Brand" and scheme_on=="Quantity": 
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
	# frappe.msgprint("In dn validate")
	# doc.schemes=[]
	# create_customerwise_item_on_dn_submit(doc,method)
	pass

	dl = frappe.db.sql("""select name,title,apply_on, valid_from, valid_upto,scheme_type from `tabScheme Management` where active=1 and valid_upto > now();""",as_dict=1, debug=1)

	# for i in range(len(doc.items)):
	# 	pass
	dn_items = []
	for raw in doc.get("items"):
		dn_items.append(raw.item_code)
		print "\n\nItem COde",raw.item_code
	print "full list",dn_items
	print "fisrt item",dn_items[0]
	item_code_for_check = dn_items[0]
	dn_customer = doc.customer

	scheme_title= frappe.db.sql("""select title from `tabScheme Management` where active=1 and valid_upto > now() and item_code=%s""",(item_code_for_check),as_dict=1, debug=1)
	print "scheme_title",scheme_title
	# frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s) 
	#  		 order by CAST(priority as UNSIGNED) desc""",(doc.posting_date,doc.posting_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)
	# gives all the schemes applicable on current  item,brand and item group irrespective of amount and quantity
	scheme_list=[]
	for i in scheme_title:
		scheme_list.append(i["title"])
	print "scheme_list",scheme_list

	scheme_obj = frappe.get_doc("Scheme Management",scheme_list[0])
	print "\napply",scheme_obj.apply_on

	available_scheme_list = []
	if scheme_obj.apply_on=="Item Code" and scheme_obj.scheme_on=="Quantity":
		# main_object_name=scheme_obj.item_code
		effective_qty=frappe.db.sql("""select sum(effective_qty) as effective_qty from `tabCustomerwise Item` 
			where customer=%s and item_code=%s""",(dn_customer,item_code_for_check),as_dict=1)
		print "effective_qty",effective_qty[0]["effective_qty"]
		effective_qty_check = effective_qty[0]["effective_qty"]

		for i in scheme_list:
			scheme_obj = frappe.get_doc("Scheme Management",i)
			#if scheme on qty
			if scheme_obj.scheme_on=="Quantity":
				if effective_qty_check>=scheme_obj.minimum_quantity and effective_qty_check>=scheme_obj.quantity:
					available_scheme_list.append(scheme_obj.title)
			elif scheme_obj.scheme_on=="Price":
				#check for price validations like on 50k give 5k free
				pass

		print "\nScheme Available",available_scheme_list
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
	frappe.msgprint("In dn get_schemes")
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
	print "full list",dn_items
	print "fisrt item",dn_items[0]
	dn_customer = doc["customer"]

	# item_code_for_check = dn_items

	available_scheme_list = []

	for raw in doc.get("items"):
		scheme_title= frappe.db.sql("""select title from `tabScheme Management` where active=1 and valid_upto > now() and item_code=%s""",(raw["item_code"]),as_dict=1, debug=1)
		print "scheme_title",scheme_title
		# frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s) 
		#  		 order by CAST(priority as UNSIGNED) desc""",(doc.posting_date,doc.posting_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)
		# gives all the schemes applicable on current  item,brand and item group irrespective of amount and quantity
		scheme_list=[]
		for i in scheme_title:
			scheme_list.append(i["title"])
		print "\n\nscheme_listttttt",scheme_list

		for i in scheme_list:
			if i:
				scheme_obj = frappe.get_doc("Scheme Management",i)
				print "\napply",scheme_obj.apply_on
				print "\n item code in dn",raw["item_code"]

	
			if scheme_obj.apply_on=="Item Code" and scheme_obj.scheme_on=="Quantity":
				# main_object_name=scheme_obj.item_code
				effective_qty=frappe.db.sql("""select sum(effective_qty) as effective_qty from `tabCustomerwise Item` 
					where customer=%s and item_code=%s""",(dn_customer,raw["item_code"]),as_dict=1)
				print "effective_qty",effective_qty[0]["effective_qty"]
				effective_qty_check = effective_qty[0]["effective_qty"]

				for i in scheme_list:
					scheme_obj = frappe.get_doc("Scheme Management",i)
					#if scheme on qty
					if scheme_obj.scheme_on=="Quantity":
						if effective_qty_check>=scheme_obj.minimum_quantity and effective_qty_check>=scheme_obj.quantity:
							available_scheme_list.append(scheme_obj.title)
					elif scheme_obj.scheme_on=="Price":
						#check for price validations like on 50k give 5k free
						pass

				print "\nScheme Available list initial",available_scheme_list

	print "available_scheme_list",available_scheme_list
	id_list = tuple([x.encode('UTF8') for x in available_scheme_list if x])	
	#remove , at the end
	if len(id_list) == 1:
		cond ="where title = '{0}' ".format(id_list[0]) 
	elif len(id_list) > 1:	
		cond = "where title in {0} ".format(id_list) 

	dl = frappe.db.sql("""select name,title,apply_on, valid_from, valid_upto,scheme_type from `tabScheme Management` {0}""".format(cond),as_dict=1, debug=1)
	print "\n\ndl",dl
	# dl = frappe.db.sql("""select name,title,apply_on, valid_from, valid_upto,scheme_type from `tabScheme Management` where active=1 and valid_upto > now();""",as_dict=1, debug=1)
	# frappe.msgprint(dl)
	return dl
	# doc_json = json.loads(doc)
	# frappe.msgprint(doc_json["name"])
	# doc_dn = frappe.get_doc("Delivery Note", doc_json["name"])
	# doc_dn.set('schemes', [])
	# for d in dl:
	# 	nl = doc_dn.append('schemes', {})
	# 	nl.apply_on = d.apply_on
	# 	nl.scheme_name = d.name
	# 	frappe.msgprint(d.apply_on)
	# doc_dn.terms="asv"
	# doc_dn.save()


	# dl = frappe.db.sql("""select name,customer,date_of_receipt, date_of_collection,job_card,functional_location,functional_location_code,
	# 			equipment,equipment_make,serial_number,equipment_code,
	# 			conservation_protection_system, sample_taken_from, oil_temperature, winding_temperature,
	# 			remarks from `tabSample Entry Register` where docstatus = 0 and order_id='%s' %s"""%(self.order, condition),as_dict=1, debug=1)

	# 		self.set('sample_entry_creation_tool_details', [])

	# 		for d in dl:
	# 			nl = self.append('sample_entry_creation_tool_details', {})
	# 			nl.sample_id = d.name
	# 			nl.customer = d.customer
	# 			nl.job_card = d.job_card
	# 			nl.functional_location=d.functional_location
	# 			nl.functional_location_code = d.functional_location_code

def create_customerwise_item_on_dn_submit(doc,method):
	if doc.is_return!=1:
		for raw in doc.get("items"):
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
			cwi.save()



		
	


		































					










						

						





			

		






			







		












		