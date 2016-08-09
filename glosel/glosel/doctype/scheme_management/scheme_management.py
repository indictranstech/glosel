# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans Technologies PVT LTD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today
from frappe import _

class SchemeManagement(Document):
	def validate(self):
		if self.scheme_depends_upon=="Company":
			self.terrritory=None
			self.customer=None
			self.customer_group=None
		elif self.scheme_depends_upon=="Territory":
			self.company=None
			self.customer=None
			self.customer_group=None
		elif self.scheme_depends_upon=="Customer":
			self.company=None
			self.territory
			self.customer_group=None
		elif self.scheme_depends_upon=="Customer Group":
			self.terrritory=None
			self.company=None
			self.customer=None
		if self.apply_on=="Item Code":
			self.brand==None
			self.item_group =None
		elif self.apply_on=="Brand":
			self.item_code==None
			self.item_group =None
		elif self.apply_on=="Item Group":
			self.item_code==None
			self.brand =None
		





