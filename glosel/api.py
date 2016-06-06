import frappe
from frappe import _
def get_supplier_uom(doctype, txt, searchfield, start, page_len, filters):
	supplier_uom = frappe.db.sql("""select  uom_name from `tabUOM` where supplier_uom= 1 """)
	return supplier_uom
@frappe.whitelist()
def fetch_supplier_uom(supplier,item):
	# frappe.throw(_("Please select supplier"))
	if supplier==None:
		frappe.throw(_("Please select supplier"))

	uom=frappe.db.get_value("Item Supplier",{"supplier":supplier,"parent":item},"uom")
	return uom 

