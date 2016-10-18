# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "glosel"
app_title = "Glosel"
app_publisher = "New Indictrans Technologies PVT LTD"
app_description = "Distributes Pharmaciticals and Cosmotics"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ravindra.l@indictranstech.com"
app_version = "0.0.1"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_js = ["assets/js/glosel.min.js"]

# include js, css files in header of desk.html
# app_include_css = "/assets/glosel/css/glosel.css"
app_include_js = "/assets/js/glosel.desk.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/glosel/css/glosel.css"
# web_include_js = "/assets/glosel/js/glosel.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "glosel.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "glosel.install.before_install"
# after_install = "glosel.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "glosel.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		"validate": ["glosel.custom_py_methods.make_title_case", "glosel.custom_py_methods.generate_calling_code"]
	},
	# "Customer": {
	# 	"validate": ["glosel.custom_py_methods.customer_validation","glosel.custom_py_methods.make_title_case"]
	# 	# "on_cancel": "method",
	# 	# "on_trash": "method"
	# },
	"Delivery Note": {
		"on_submit": ["glosel.custom_py_methods.delivery_note_submit","glosel.scheme_management.dn_submit","glosel.scheme_management.distributer_outstanding_add","glosel.scheme_management.dn_return_submit"],
		"on_cancel":"glosel.scheme_management.dn_on_cancel",
		"validate":"glosel.scheme_management.dn_validate",
		"before_submit":"glosel.scheme_management.dn_before_submit"
		# "on_update": ["glosel.scheme_management.dn_update"]
		# "on_trash": "method"
	},
	"Purchase Order": {
		# "on_submit": ["glosel.custom_py_methods.delivery_note_submit","glosel.scheme_management.dn_submit","glosel.scheme_management.distributer_outstanding_add","glosel.scheme_management.dn_return_submit"],
		# "on_cancel":"glosel.scheme_management.dn_on_cancel",
		"before_submit":"glosel.scheme_management.po_before_submit",
		# "before_submit":"glosel.scheme_management.dn_before_submit"
		# "validate": "glosel.scheme_management.po_before_submit_create_so"
		# "on_trash": "method"
	},
	"Leave Application": {
		"on_submit": "glosel.custom_py_methods.leaveapplication_submit",
		# "on_cancel": "method",
		# "on_trash": "method"
	},
	"Sales Order": {
	    "validate":["glosel.custom_py_methods.so_validate","glosel.scheme_management.so_validate"],
		"on_update":"glosel.scheme_management.so_update",
		# "after_save":"glosel.scheme_management.remove_rows",
		# "on_update_after_submit":"glosel.scheme_management.dn_on_update_after_submit",
		"before_submit":"glosel.scheme_management.so_before_submit",
		"on_submit":"glosel.scheme_management.so_submit",
		# "on_trash": "method"
	},
	# "Employee": {
		#"validate": "glosel.custom_py_methods.make_title_case"
		#"autoname": "glosel.custom_py_methods.employee_autoname",
		# "on_cancel": "method",
		# "on_trash": "method"
	# },
	"Employment Type": {
		"validate": "glosel.custom_py_methods.employement_type_code_check",
		# "on_cancel": "method",
		# "on_trash": "method"
	},
	# "User": {
	# 	"validate": "glosel.custom_py_methods.make_title_case"
	# },
	# "Supplier": {
	# 	"validate": "glosel.custom_py_methods.make_title_case"
	# },
	# "Lead": {
	# 	"validate": "glosel.custom_py_methods.make_title_case"
	# },
	# "Contact": {
	# 	"validate": "glosel.custom_py_methods.make_title_case"
	# },
	# "Sales Person": {
	# 	"validate": "glosel.custom_py_methods.make_title_case"
	# },
	# "Sales Partner": {
	# 	"validate": "glosel.custom_py_methods.make_title_case"
	# }
	# "Item": {
	# 	"before_insert":
	# 	# "on_cancel": "method",
	# 	# "on_trash": "method"
	# },
	
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"glosel.tasks.all"
# 	],
# 	"daily": [
# 		"glosel.tasks.daily"
# 	],
# 	"hourly": [
# 		"glosel.tasks.hourly"
# 	],
# 	"weekly": [
# 		"glosel.tasks.weekly"
# 	]
# 	"monthly": [
# 		"glosel.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "glosel.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "glosel.event.get_events"
# }

fixtures=['Custom Script','Property Setter','Custom Field','Print Format','Role','Customer Group','Naming Series']
