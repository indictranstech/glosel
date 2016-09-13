
import frappe
import frappe.defaults
from frappe import _
def so_validate(doc,method):
	pass
	
	
def so_update(doc,method):
	pass

	# print "on  update code -------------------------------------"
	
	
	# for raw in doc.get("items"):
		
	# 	if raw.is_free_item==0 and customer.customer_group!="Distributer":
	# 		item=frappe.get_doc("Item",raw.item_code)
	# 		item_code=raw.item_code
	# 		item_group=item.item_group
	# 		brand=item.brand
	# 		so_customer=doc.customer
	# 		customer_group=doc.customer_group

	# 		qty=raw.qty
	# 		scheme_title=frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s)
	# 		 order by CAST(priority as UNSIGNED) desc  limit 1""",(doc.transaction_date,doc.transaction_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)
	# 		for i in scheme_title:
	# 			if i :
	# 				scheme_name=i.get("title")
	# 				raw.scheme=scheme_name
	# 				scheme=frappe.get_doc("Scheme Management",scheme_name)
	# 				if int(qty)>=int(scheme.minimum_quantity):
	# 					raw.description=None
	# 					for scheme_raw in scheme.get("freebie_items"):
	# 						free_items = doc.append('free_items', {})
	# 						free_items.is_free_item=1
	# 						free_items.item_code=scheme_raw.item_code
	# 						free_items.item_name=scheme_raw.item_name
	# 						if doc.company==frappe.defaults.get_defaults().get("company"):
	# 							free_items.warehouse=frappe.db.get_value("Item",{"item_code":raw.item_code},"default_warehouse")
	# 						else:
	# 							free_items.warehouse="Finished Goods" + " " + "-" + " " + doc.company[0:5]
	# 						free_items.free_with=raw.item_code
	# 						free_items.scheme=scheme_name
	# 						free_items.description="Free with Minimum {0} {1}".format(scheme.minimum_quantity,scheme.item_name)
	# 						new_qty=find_divisible_number(int(qty),int(scheme.minimum_quantity))
	# 						real_quantity=int((new_qty*scheme_raw.quantity)/scheme.minimum_quantity)
							
	# 						free_items.qty=real_quantity
	# 						if raw.description==None:
	# 							raw.description="Free {0} {1}  ".format(free_items.qty,free_items.item_name)
	# 						else:
	# 							raw.description=raw.description +"\n Free {0} {1}  ".format(free_items.qty,free_items.item_name)

	# 						free_items.rate=0
	# 						free_items.save()
		
def so_before_submit(doc,method):
	pass
	# print "on submitt-!!!!!!!!!!!!!!!!!!!!!!!!!!--------------"
	# doc.flag=1
	# roles=frappe.get_roles(frappe.session.user)
	# if " Scheme Manager" not in roles and doc.request_scheme_removal==1:
	# 	frappe.throw(_("You can not submit Sales order when scheme removal Request is marked"))

	# for raw in doc.get("free_items"):
	# 	fi=doc.append("items")
	# 	fi.is_free_item=raw.is_free_item
	# 	fi.item_code=raw.item_code
	# 	fi.item_name=raw.item_name
	# 	fi.warehouse=raw.warehouse
	# 	fi.free_with=raw.free_with
	# 	fi.scheme=raw.scheme
	# 	fi.description=raw.description
	# 	fi.qty=raw.qty
	# 	fi.save()
	# 	doc.free_items=[]
		# fi.save()
	
	# doc.save()
	# print "dsaaaaaaaaaaaa"
def so_submit(doc,method):
	pass
	# print "SUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUuubmit"
	
	


	

	

# def remove_free_items(doc, method):
# 	print "remobe sahjkhaddhjkshjk"
# 	doc.free_items = []

	


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
				# item_totalqty=frappe.db.sql("""select sum(dni.qty) from `tabDelivery Note` dn ,`tabDelivery Note Item` dni  where month(dn.posting_date)=month(curdate())  and dn.name=dni.parent and dn.customer=%s  and dn.docstatus=1  and dni.item_code=%s group by dni.item_code""",(doc.customer,item_code))
				# brand_total_qty=frappe.db.sql("""select sum(dni.qty) from `tabDelivery Note` dn ,`tabDelivery Note Item` dni  where month(dn.posting_date)=month(curdate())  and dn.name=dni.parent and dn.customer=%s  and dn.docstatus=1  and dni.brand=%s group by dni.brand""",(doc.customer,brand))
				# item_group_total_qty=frappe.db.sql("""select sum(dni.qty) from `tabDelivery Note` dn ,`tabDelivery Note Item` dni  where month(dn.posting_date)=month(curdate())  and dn.name=dni.parent and dn.customer=%s  and dn.docstatus=1  and dni.item_group=%s group by dni.item_group""",(doc.customer,brand))
				# item_amount=None
				# brand_amount=None
				# item_group_amount=None
				
				scheme_title=frappe.db.sql("""select title from `tabScheme Management` where  active = 1 and date(valid_from)<=%s and date(valid_upto)>=%s and (item_code=%s or item_group=%s or brand=%s) and (company=%s or territory=%s or customer=%s or customer_group=%s) 
	 		 order by CAST(priority as UNSIGNED) desc""",(doc.posting_date,doc.posting_date,item_code,item_group,brand,customer_company,company_territory,so_customer,customer_group),as_dict=1)

				for i in scheme_title:
					if i :
						scheme_name=i.get("title")
						frappe.errprint(scheme_name)
				scheme_obj=frappe.get_doc("Scheme Management",scheme_name)
				if scheme_obj.apply_on=="Item Group":
					main_object_name=scheme_obj.item_group
				elif scheme_obj.apply_on=="Item Code":
					main_object_name=scheme_obj.item_code
				else: 
					main_object_name=scheme_obj.brand
				main_object_criteria=scheme_obj.apply_on
				for scheme_raw in scheme_obj.get("freebie_items"):
					free_object_criteria=scheme_raw.apply_on
					# free_object_name=scheme_raw.


					# 	entries = frappe.db.get_all("Customer Scheme Record",
    	# 	filters={"customer":doc.customer, "main_object_name":main_object_name},
  			# fields=["name"])
				 

	


def dn_update(doc,method):
	pass
	# print "on dn update code -------------------------------------"
	# if doc.is_return==1:
	# 	fflag=0
	# 	depend_doc=frappe.get_doc("Delivery Note",doc.return_against)
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
	print "on dn return code -------------------------------------"
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
	print "on  find_divisible_number -------------------------------------"
	for i in range(qty,sc_min_qty-1,-1):
		if i%sc_min_qty==0:
			return i

def dn_on_cancel(doc,method):
	print "on  cancwel -------------------------------------"
	if doc.company!=frappe.defaults.get_defaults().get("company") and doc.is_return==0:
		# if doc.company !="Glosel India PVT LTD":
		for raw in doc.get("items"):
			if raw.is_free_item==1:
				item_doc=frappe.get_doc("Item",raw.item_code)
				for raw1 in item_doc.get("distributer_outstanding"):
					if raw1.company==doc.company:
						raw1.qty=raw1.qty-raw.qty
						item_doc.save()

def remove_rows(doc,method):
	pass

	# frappe.errprint ("on  remove -------------------------------------")
	# to_remove=[]
	# for raw in doc.get("items"):
	# 	to_remove.append(raw)
	# for d in to_remove:
	# 	doc.remove(d) 
	# # doc.save()
	# # doc.remove('free_items')
	# doc.save()
def dn_validate(doc,method):
	pass
def create_new_doc_dn_before_submit(doc,method):
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
			cwi.save()



		
	


		































					










						

						





			

		






			







		












		