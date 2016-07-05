# Copyright (c) 2013, New Indictrans Technologies PVT LTD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), []
	return columns, data
def get_columns():
	return [_("Date") + ":Datetime:95",_("Company") + ":Link/Company:100", _("Item") + ":Link/Item:130", _("Item Name") + "::100", _("Item Group") + ":Link/Item Group:100",
		_("Brand") + ":Link/Brand:100", 
		 _("Qty") + ":Float:50",_("Free Item") +  ":Link/Item:130",_("Brand") + ":Link/Brand:100", 
		 _("Qty") + ":Float:50",_("Return Quantity") + ":Float:50"
		
	]

