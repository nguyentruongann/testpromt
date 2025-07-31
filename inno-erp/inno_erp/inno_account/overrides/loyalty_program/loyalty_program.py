import frappe
from erpnext.accounts.doctype.loyalty_program import loyalty_program
from erpnext.accounts.doctype.loyalty_program.loyalty_program import (
	LoyaltyProgram,
	get_loyalty_details,
	get_loyalty_program_details,
)
from frappe import _
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Sum
from frappe.utils import today


class InnoLoyaltyProgram(LoyaltyProgram):
	pass


def get_loyalty_details(
	customer,
	loyalty_program,
	expiry_date=None,
	company=None,
	include_expired_entry=False,
):
	if not expiry_date:
		expiry_date = today()

	loyalty_point_entry = DocType("Loyalty Point Entry")

	query = (
		frappe.qb.from_(loyalty_point_entry)
		.select(
			Sum(loyalty_point_entry.loyalty_points).as_("loyalty_points"),
			Sum(loyalty_point_entry.purchase_amount).as_("total_spent"),
			Count(loyalty_point_entry.name).as_("total_orders"),
		)
		.where(loyalty_point_entry.customer == customer)
		.where(loyalty_point_entry.loyalty_program == loyalty_program)
		.where(loyalty_point_entry.posting_date <= expiry_date)
	)

	if company:
		query = query.where(loyalty_point_entry.company == company)
	if not include_expired_entry:
		query = query.where(loyalty_point_entry.expiry_date >= expiry_date)

	query = query.groupby(loyalty_point_entry.customer)
	loyalty_point_details = query.run(as_dict=True)

	if loyalty_point_details:
		return loyalty_point_details[0]
	else:
		return {"loyalty_points": 0, "total_spent": 0, "total_orders": 0}

loyalty_program.get_loyalty_details = get_loyalty_details

@frappe.whitelist()
def get_loyalty_program_details_with_points(
	customer,
	loyalty_program=None,
	expiry_date=None,
	company=None,
	silent=False,
	include_expired_entry=False,
	current_transaction_amount=0,
):
	lp_details = get_loyalty_program_details(customer, loyalty_program, company=company, silent=silent)
	loyalty_program = frappe.get_doc("Loyalty Program", loyalty_program)

	lp_details.update(
		get_loyalty_details(customer, loyalty_program.name, expiry_date, company, include_expired_entry)
	)

	tier_spent_level = sorted(
		[doc.as_dict() for doc in loyalty_program.collection_rules],
		key=lambda rule: rule.min_spent,
	)
	for idx, doc in enumerate(tier_spent_level):
		if idx == 0 or (
			lp_details.total_spent >= doc.min_spent
			and lp_details.total_orders >= doc.custom_minimum_total_orders
		):
			lp_details.tier_name = doc.tier_name
			lp_details.collection_factor = doc.collection_factor
		else:
			break
	return lp_details


loyalty_program.get_loyalty_program_details_with_points = get_loyalty_program_details_with_points


def update_customer_rank(customer):
	customer_doc = frappe.get_doc("Customer", customer)
	loyalty_point_entry = DocType("Loyalty Point Entry")

	customer_data = (
		frappe.qb.from_(loyalty_point_entry)
		.select(
			Sum(loyalty_point_entry.purchase_amount).as_("total_spent_customer"),
			Count(loyalty_point_entry.name).as_("total_orders_customer"),
		)
		.where(loyalty_point_entry.customer == customer_doc.name)
		.where(loyalty_point_entry.loyalty_program == customer_doc.loyalty_program)
	).run(as_dict=True)
	total_spent_customer = customer_data[0]["total_spent_customer"] if customer_data else 0
	total_orders_customer = customer_data[0]["total_orders_customer"] if customer_data else 0

	loyalty_program = frappe.get_doc("Loyalty Program", customer_doc.loyalty_program)

	tier_spent_level = sorted(
		[d.as_dict() for d in loyalty_program.collection_rules],
		key=lambda rule: rule.min_spent,
	)
	len_of_tier = len(tier_spent_level)
	index = 0
	while index < len_of_tier:
		if index == 0 or (
			total_spent_customer >= tier_spent_level[index].min_spent
			and total_orders_customer >= tier_spent_level[index].custom_minimum_total_orders
		):
			customer_doc.custom_rank = tier_spent_level[index].tier_name
			if index == len_of_tier - 1:
				customer_doc.save()
			index += 1
		else:
			customer_doc.save()
			break


@frappe.whitelist()
def get_loyalty_program_rules(loyalty_program):
	LoyaltyProgramCollection = DocType("Loyalty Program Collection")
	return (
		frappe.qb.from_(LoyaltyProgramCollection)
		.select(
			LoyaltyProgramCollection.tier_name,
			LoyaltyProgramCollection.min_spent,
			LoyaltyProgramCollection.custom_minimum_total_orders,
			LoyaltyProgramCollection.custom_rate,
			LoyaltyProgramCollection.collection_factor,
		)
		.where(LoyaltyProgramCollection.parent == loyalty_program)
		.orderby(LoyaltyProgramCollection.min_spent)
		.run(as_dict=True)
	)

@frappe.whitelist()
def get_all_loyalty_program():
	loyalty_program = frappe.db.get_all("Loyalty Program", fields=["name"])

	for program in loyalty_program:
		program.collection_rules = get_loyalty_program_rules(program.name)
	return loyalty_program

def determine_customer_tier(loyalty_collection_rules, total_spent, total_orders):
	current_tier = None
	current_tier_index = -1
	for idx, tier in enumerate(loyalty_collection_rules):
		if total_spent >= tier.min_spent and total_orders >= tier.get("custom_minimum_total_orders", 0):
			current_tier = tier
			current_tier_index = idx

	if current_tier is None and loyalty_collection_rules:
		current_tier = loyalty_collection_rules[0]
		current_tier_index = 0

	return current_tier, current_tier_index


def calculate_next_tier_details(
	loyalty_collection_rules, current_tier_index, total_spent, total_orders
):
	next_tier = None
	requirements = {}
	if 0 <= current_tier_index < len(loyalty_collection_rules) - 1:
		next_tier = loyalty_collection_rules[current_tier_index + 1]
		requirements = {
			"spent_needed": max(0, next_tier.min_spent - total_spent),
			"orders_needed": max(0, next_tier.get("custom_minimum_total_orders", 0) - total_orders),
			"next_tier_name": next_tier.tier_name,
			"next_tier_min_spent": next_tier.min_spent,
			"next_tier_min_orders": next_tier.get("custom_minimum_total_orders", 0),
		}
	return next_tier, requirements

@frappe.whitelist()
def get_customer_loyalty_tier_info(customer, company=None):
	try:
		customer_doc = frappe.get_doc("Customer", customer)
		if not customer_doc.loyalty_program:
			frappe.throw(_("Customer has not joined any loyalty program"))

		loyalty_program_name = customer_doc.loyalty_program
		loyalty_details = get_loyalty_details(
			customer=customer,
			loyalty_program=loyalty_program_name,
			company=company,
			include_expired_entry=False,
		)

		total_spent = loyalty_details.get("total_spent", 0)
		total_orders = loyalty_details.get("total_orders", 0)

		loyalty_program_doc = frappe.get_doc("Loyalty Program", loyalty_program_name)
		loyalty_collection_rules = get_loyalty_program_rules(loyalty_program_name)

		current_tier, current_tier_index = determine_customer_tier(
			loyalty_collection_rules, total_spent, total_orders
		)

		next_tier, requirements_for_next_tier = calculate_next_tier_details(
			loyalty_collection_rules, current_tier_index, total_spent, total_orders
		)

		result = {
			"customer": customer,
			"customer_name": customer_doc.customer_name,
			"loyalty_program_name": loyalty_program_name,
			"current_stats": {
				"total_spent": total_spent,
				"total_orders": total_orders,
				"loyalty_points": loyalty_details.get("loyalty_points", 0),
			},
			"current_tier": {
				"tier_name": current_tier.tier_name if current_tier else None,
				"collection_factor": current_tier.collection_factor if current_tier else 0,
				"min_spent": current_tier.min_spent if current_tier else 0,
				"min_orders": current_tier.get("custom_minimum_total_orders", 0) if current_tier else 0,
			},
			"next_tier": next_tier.tier_name if next_tier else None,
			"next_tier_requirements": requirements_for_next_tier or None,
			"conversion_factor": loyalty_program_doc.conversion_factor,
			"company": company,
		}

		return result

	except Exception as e:
		frappe.throw(_("Error: {0}").format(str(e)))
