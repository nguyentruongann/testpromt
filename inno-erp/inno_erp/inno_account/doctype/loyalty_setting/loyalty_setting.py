# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

from datetime import timedelta

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, now_datetime, nowdate


class LoyaltySetting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		date_1: DF.Date | None
		date_2: DF.Date | None
		date_3: DF.Date | None
		method: DF.Literal["To Default Rank", "Demote One Rank"]
	# end: auto-generated types
	pass


def reset_loyalty_points():
	setting = frappe.get_single("Loyalty Setting")
	method = setting.method
	now_date = nowdate()

	reset_point = setting.date_1 == now_date or setting.date_2 == now_date or setting.date_3 == now_date

	if not reset_point:
		return

	if method == "To Default Rank":
		to_default_rank()
	else:
		demote_one_rank()

	frappe.db.set_value(
		"Loyalty Point Entry",
		{},
		{
			"expiry_date": now_date - timedelta(days=1),
		},
	)


def to_default_rank():
	loyalty_point_entry = frappe.db.get_list(
		"Loyalty Point Entry",
		limit=1,
		order_by="posting_date desc",
		fields=["name", "customer", "loyalty_program"],
	)
	loyalty_program = frappe.get_doc("Loyalty Program", loyalty_point_entry[0].loyalty_program)
	if loyalty_program:
		tier_spent_level = sorted(
			[d.as_dict() for d in loyalty_program.collection_rules],
			key=lambda rule: rule.min_spent,
		)
		frappe.db.set_value("Customer", {}, "custom_rank", tier_spent_level[0].tier_name)


def demote_one_rank():
	pass
	# TODO: review
	# loyalty_point_entry = frappe.db.get_list(
	# 	"Loyalty Point Entry",
	# 	order_by="posting_date desc",
	# 	fields=["name", "customer", "loyalty_program"],
	# 	limit=1,
	# )
	# loyalty_program = (
	# 	frappe.get_doc("Loyalty Program", loyalty_point_entry[0].loyalty_program)
	# 	if loyalty_point_entry
	# 	else None
	# )
	# if loyalty_program:
	# 	tier_spent_level = sorted(
	# 		[d.as_dict() for d in loyalty_program.collection_rules],
	# 		key=lambda rule: rule.min_spent,
	# 	)
	# 	rank_demotion_map = {}
	# 	Customers = frappe.db.get_list("Customer", fields=["name", "custom_rank"])
	# 	for i in range(1, len(tier_spent_level)):
	# 		current_tier_id = tier_spent_level[i].tier_name
	# 		previous_tier_id = tier_spent_level[i - 1].tier_name
	# 		rank_demotion_map[current_tier_id] = previous_tier_id
	# 	for c in Customers:
	# 		if c.custom_rank in rank_demotion_map:
	# 			new_rank = rank_demotion_map[c.custom_rank]
	# 			frappe.db.set_value("Customer", c.name, "custom_rank", new_rank)
