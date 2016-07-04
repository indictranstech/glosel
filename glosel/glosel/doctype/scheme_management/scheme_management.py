# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans Technologies PVT LTD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SchemeManagement(Document):
	def validate(self):
		if self.scheme_depends_upon=="Company":
			self.terrritory=None
		elif self.scheme_depends_upon=="Territory":
			self.company=None
		# if self.apply_on=="Item Code":
		# 	self.brand==None
		# 	self.item_group =None
		# elif self.apply_on=="Brand":
		# 	self.item_code==None
		# 	self.item_group =None
		# elif self.apply_on=="Item Group":
		# 	self.item_code==None
		# 	self.brand =None
		





