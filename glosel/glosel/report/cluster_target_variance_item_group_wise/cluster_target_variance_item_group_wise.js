// Copyright (c) 2016, New Indictrans Technologies PVT LTD and contributors
// For license information, please see license.txt

frappe.query_reports["Cluster Target Variance Item Group-Wise"] = {
	"filters": [
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: sys_defaults.fiscal_year
		},
		{
			fieldname: "period",
			label: __("Period"),
			fieldtype: "Select",
			options: [
				{ "value": "Monthly", "label": __("Monthly") },
				{ "value": "Quarterly", "label": __("Quarterly") },
				{ "value": "Half-Yearly", "label": __("Half-Yearly") },
				{ "value": "Yearly", "label": __("Yearly") }
			],
			default: "Monthly"
		},
		{
			fieldname: "target_on",
			label: __("Target On"),
			fieldtype: "Select",
			options: "Quantity\nAmount",
			default: "Quantity"
		},
	]
}
