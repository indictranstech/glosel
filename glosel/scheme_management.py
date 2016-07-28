
import frappe
import frappe.defaults
from frappe import _

def so_submit(doc,method):
	# print " default company is " ,frappe.defaults.get_defaults().get("company")
	# end customer object
	customer=frappe.get_doc("Customer",doc.customer)
	# gives distributor name who is actually a company to end customer
	customer_company=doc.company
	if customer_company!=frappe.defaults.get_defaults().get("company"):
	# if customer_company!="Glosel India PVT LTD":
	# gives distributer object which is actually a company on SO to find the terretory of distributor
		company=frappe.get_doc("Customer",customer_company)
		# distributer's terretory as the end customer's terretory and customer's terretory will be same
		company_territory=company.territory 
	else:
		company= frappe.defaults.get_defaults().get("company")
		# company="Glosel India PVT LTD"
		glosel_object=frappe.get_doc("Company",frappe.defaults.get_defaults().get("company"))
		# glosel_object=frappe.get_doc("Company","Glosel India PVT LTD")
		company_territory=customer.territory
	for raw in doc.get("items"):
		
		if raw.is_free_item==0 and customer.customer_group!="Distributer":
			# raw.description=None
			item=frappe.get_doc("Item",raw.item_code)
			item_code=raw.item_code
			item_group=item.item_group
			brand=item.brand
			qty=raw.qty
			scheme_title=frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and item_code=%s and (company=%s or territory=%s)
			 order by CAST(priority as UNSIGNED) desc  limit 1""",(doc.transaction_date,doc.transaction_date,item_code,customer_company,company_territory),as_dict=1)
			for i in scheme_title:
				if i :
					scheme_name=i.get("title")
					frappe.errprint(scheme_name)
					raw.scheme=scheme_name
					# frappe.errprint("Applied Scheme")
					# frappe.errprint(raw.scheme)
					scheme=frappe.get_doc("Scheme Management",scheme_name)
					# frappe.errprint(scheme_name)
					if int(qty)>=int(scheme.minimum_quantity):
						raw.description=None
						for scheme_raw in scheme.get("freebie_items"):
							free_items = doc.append('items', {})
							free_items.is_free_item=1
							free_items.item_code=scheme_raw.item_code
							free_items.item_name=scheme_raw.item_name
							if doc.company==frappe.defaults.get_defaults().get("company"):
								free_items.warehouse=frappe.db.get_value("Item",{"item_code":raw.item_code},"default_warehouse")
							else:
								free_items.warehouse="Finished Goods" + " " + "-" + " " + doc.company[0:5]
							# Source item name
							free_items.free_with=raw.item_code
							free_items.scheme=scheme_name
							free_items.description="Free with Minimum {0} {1}".format(scheme.minimum_quantity,scheme.item_name)
							new_qty=find_divisible_number(int(qty),int(scheme.minimum_quantity))
							real_quantity=int((new_qty*scheme_raw.quantity)/scheme.minimum_quantity)
							# real_quantity=int((qty*scheme_raw.quantity)/scheme.minimum_quantity)
							# modulas=0
							# if qty > scheme.minimum_quantity:

							# 	modulas=real_quantity%scheme.minimum_quantity
							# 	if real_quantity<scheme.minimum_quantity:
							# 		modulas=0
					
							# free_items.qty=real_quantity-(modulas)
							free_items.qty=real_quantity
							if raw.description==None:
								raw.description="Free {0} {1}  ".format(free_items.qty,free_items.item_name)
							else:
								raw.description=raw.description +"\n Free {0} {1}  ".format(free_items.qty,free_items.item_name)

							free_items.rate=0

							free_items.save()
							# doc.save()


def distributer_outstanding_add(doc,method):
	"""called on dn submit"""
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
	for raw in doc.get("items"):
		if raw.is_free_item==1:
			sml=frappe.new_doc("Scheme Management Log")
			sml.date=doc.posting_date
			sml.distributer=doc.company
			sml.dn=doc.name
			item_obj=frappe.get_doc("Item",raw.free_with)
			sml.item=item_obj.item_code
			for raw1 in doc.get("items"):
				if raw1.item_code==sml.item and raw1.is_free_item!=1:
					sml.item_qty=raw1.qty
			sml.free_item=raw.item_code
			sml.free_item_qty=raw.qty
			sml.scheme=raw.scheme
			sml.save()
			sml.submit()

def dn_update(doc,method):
	if doc.is_return==1:
		fflag=0
		depend_doc=frappe.get_doc("Delivery Note",doc.return_against)
		# for i in range(len(doc.items)):
		# 	# frappe.errprint (i)
		# 	if (doc.items[i].item_code==depend_doc.items[i].item_code) and (doc.items[i].rate==depend_doc.items[i].rate):
		# 		frappe.errprint(depend_doc.items[i].qty)
		# 		frappe.errprint(doc.items[i].qty)
		# 		if depend_doc.items[i].is_free_item and depend_doc.items[i].qty>abs(doc.items[i].qty):
		# 			fflag=1
		# 		# frappe.errprint(fflag)
		# 		if fflag==1:
		# 			frappe.throw("You can not return only free Items")

def dn_return_submit(doc,method):
	# frappe.errprint("Inside DN return uodate")
	if doc.is_return==1:
		depend_doc=frappe.get_doc("Delivery Note",doc.return_against)
		for i in range(len(doc.items)):
			if (doc.items[i].item_code==depend_doc.items[i].item_code) and (doc.items[i].rate==depend_doc.items[i].rate) and (not doc.items[i].is_free_item) and (depend_doc.items[i].qty>abs(doc.items[i].qty)):
				scheme_name=doc.items[i].scheme
				scheme=frappe.get_doc("Scheme Management",scheme_name)
				# actual quantity of original item
				actual_item_qty=doc.items[i].qty+depend_doc.items[i].qty
				# scheme_item_list=[]
				# for freebie in scheme.get("freebie_items"):
				# 	item_code=freebie.item_code
				# 	qty=freebie.quantity
					# scheme_item_dict={"item_code":item_code,"qty":qty}
					# scheme_item_list.append(scheme_item_dict)
					# total remaining actual items after return. Now can calculate no.of free items on this qty and compare with remaining qty
					
					# real_quantity=int((qty*scheme_raw.quantity)/scheme.minimum_quantity)
					# modulas=real_quantity%scheme.minimum_quantity
					# if real_quantity<scheme.minimum_quantity:
					# 	modulas=0
				# finding free items with current items
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
	for i in range(qty,sc_min_qty-1,-1):
		if i%sc_min_qty==0:
			return i

def dn_on_cancel(doc,method):
	if doc.company!=frappe.defaults.get_defaults().get("company") and doc.is_return==0:
		# if doc.company !="Glosel India PVT LTD":
		for raw in doc.get("items"):
			if raw.is_free_item==1:
				item_doc=frappe.get_doc("Item",raw.item_code)
				for raw1 in item_doc.get("distributer_outstanding"):
					if raw1.company==doc.company:
						raw1.qty=raw1.qty-raw.qty
						item_doc.save()


@frappe.whitelist()
def onload_dn_return():
	pass



























					










						

						





			

		






			







		












		