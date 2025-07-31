import frappe
from erpnext import get_default_company
from erpnext.accounts.utils import get_balance_on
from frappe import _
from frappe.utils import flt, formatdate, get_first_day, get_last_day, getdate, nowdate

CASH_ACCOUNT_NUMBER = "1111"
BANK_ACCOUNT_NUMBER = "1121"

CHART_COLORS = {
	"green": "#30a66d",  # --green-600 (Receive/Inflow)
	"red": "#e03636",  # --red-600 (Pay/Outflow)
}


def execute(filters=None):
	filters = frappe._dict(get_default_filter(filters))
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data, filters)
	summary = get_summary_data(data, filters)

	return columns, data, None, chart, summary


def get_columns():
	return [
		{
			"fieldname": "reference_doctype",
			"label": _("Transaction Type"),
			"fieldtype": "Link",
			"options": "Doctype",
			"width": 175,
			"align": "left",
		},
		{
			"fieldname": "reference_name",
			"label": _("Transaction"),
			"fieldtype": "Dynamic Link",
			"options": "reference_doctype",
			"width": 200,
			"align": "left",
		},
		{
			"fieldname": "due_date",
			"label": _("Transaction Date"),
			"fieldtype": "Date",
			"width": 200,
			"align": "left",
		},
		{
			"fieldname": "party_type",
			"label": _("Party Type"),
			"fieldtype": "Data",
			"width": 200,
			"align": "left",
		},
		{
			"fieldname": "party_name",
			"label": _("Party Name"),
			"fieldtype": "Data",
			"width": 200,
			"align": "left",
		},
		{
			"fieldname": "payment_type",
			"label": _("Payment Type"),
			"fieldtype": "Data",
			"width": 150,
			"align": "center",
		},
		{
			"fieldname": "mode_of_payment",
			"label": _("Mode of Payment"),
			"fieldtype": "Data",
			"width": 150,
			"align": "left",
		},
		{
			"fieldname": "income",
			"label": _("Income"),
			"fieldtype": "Currency",
			"width": 200,
			"align": "right",
		},
		{
			"fieldname": "expense",
			"label": _("Expense"),
			"fieldtype": "Currency",
			"width": 200,
			"align": "right",
		},
	]


def get_data(filters):
	payment_refs = collect_payment_refs(filters)
	for ref in payment_refs:
		if ref.get("payment_type") == "Receive":
			ref.income = ref.total_amount
		elif ref.get("payment_type") == "Pay":
			ref.expense = abs(ref.total_amount)

		# WARN: should be translated before return
		if ref.get("party_type"):
			ref.party_type = _(ref.get("party_type"))
		ref.reference_doctype = _(ref.get("reference_doctype"))
		ref.payment_type = _(ref.get("payment_type"))

	return payment_refs


def collect_payment_refs(filters):
	pe = frappe.qb.DocType("Payment Entry")
	pe_ref = frappe.qb.DocType("Payment Entry Reference")
	query = (
		frappe.qb.from_(pe_ref)
		.left_join(pe)
		.on(pe_ref.parent == pe.name)
		.select(
			pe_ref.reference_doctype,
			pe_ref.reference_name,
			pe_ref.due_date,
			pe_ref.total_amount,
			pe.payment_type,
			pe.mode_of_payment,
			pe.party_type,
			pe.party_name,
			pe.cost_center,
		)
		.where(pe_ref.docstatus == 1)
		.orderby(pe_ref.due_date, pe_ref.creation)
	)

	query = query.where(
		(pe.company == filters.get("company"))
		& (pe_ref.due_date >= filters.get("from_date"))
		& (pe_ref.due_date <= filters.get("to_date"))
	)

	if filters.get("mode_of_payments"):
		mode_of_payment_list = filters.get("mode_of_payments")
		if mode_of_payment_list:
			query = query.where(pe.mode_of_payment.isin(mode_of_payment_list))

	if filters.get("payment_types"):
		payment_type_list = filters.get("payment_types")
		if payment_type_list:
			query = query.where(pe.payment_type.isin(payment_type_list))

	if filters.get("party_types"):
		party_type_list = filters.get("party_types")
		if party_type_list:
			query = query.where(pe.party_type.isin(party_type_list))

	if filters.get("parties"):
		party_list = filters.get("parties")
		if party_list:
			query = query.where(pe.party.isin(party_list))

	results = query.run(as_dict=True)
	for row in results:
		row["branch"] = frappe.db.get_value("Branch", {"custom_cost_center": row.get("cost_center")}, "name")
	return results


def get_default_filter(filters):
	if not filters:
		filters = {}

	if not filters.get("company"):
		filters["company"] = get_default_company()

	if not filters.get("from_date"):
		filters["from_date"] = get_first_day(nowdate())

	if not filters.get("to_date"):
		filters["to_date"] = get_last_day(nowdate())

	return filters


def get_chart_data(data, filters):
	if not data:
		return None

	chart = filters.get("chart", "cash_flow_trend")

	if chart == "cash_flow_trend":
		return get_cash_flow_trend_chart(data, filters)
	elif chart == "balance_trend":
		return get_balance_trend_chart(data, filters)
	elif chart == "income_expense_comparison":
		return get_income_expense_comparison_chart(data, filters)
	elif chart == "daily_bar_comparison":
		return get_daily_bar_comparison_chart(data, filters)
	elif chart == "weekly_summary":
		return get_weekly_summary_chart(data, filters)
	else:
		return get_cash_flow_trend_chart(data, filters)


def get_summary_data(data, filters):
	if not data:
		return []

	# Filter by cost center
	# cash_balance = get_current_account_balance(filters, [CASH_ACCOUNT_NUMBER])
	# bank_balance = get_current_account_balance(filters, [BANK_ACCOUNT_NUMBER])
	# cash_balance = 0.0
	# bank_balance = 0.0

	# branch_filter = get_filter_list(filters.get("branch")) if filters and filters.get("branch") else None

	total_income = total_expense = 0

	for row in data:
		# if branch_filter and not check_branch_match(row, branch_filter):
		# 	continue

		total_income += flt(row.get("income", 0))
		total_expense += flt(row.get("expense", 0))

	return [
		# {
		# 	"value": cash_balance,
		# 	"label": _("Cash Balance"),
		# 	"indicator": "Blue" if cash_balance >= 0 else "Red",
		# 	"datatype": "Currency",
		# },
		# {
		# 	"value": bank_balance,
		# 	"label": _("Bank Balance"),
		# 	"indicator": "Blue" if bank_balance >= 0 else "Red",
		# 	"datatype": "Currency",
		# },
		{"value": total_income, "label": _("Total Income"), "indicator": "Green", "datatype": "Currency"},
		{"value": total_expense, "label": _("Total Expense"), "indicator": "Red", "datatype": "Currency"},
	]


# ----------------------------------------Display Function------------------------------------------------
# def get_party_display_name(party, party_name):
# 	if not party:
# 		return ""
# 	return party_name or party


# def get_branch_display_name(branch_name):
# 	if not branch_name:
# 		return ""
# 	try:
# 		branch_title = frappe.db.get_value("Branch", branch_name, "branch")
# 		return branch_title or branch_name
# 	except:
# 		return branch_name


# def get_account_display_name(account_name):
# 	if not account_name:
# 		return ""
# 	try:
# 		account_number = frappe.db.get_value("Account", account_name, "account_number")
# 		return account_number or account_name
# 	except:
# 		return account_name


# ----------------------------------------Chart Function-------------------------------------------------
def get_cash_flow_trend_chart(data, filters):
	date_wise_data = {}
	# branch_filter = get_filter_list(filters.get("branch")) if filters and filters.get("branch") else None

	for row in data:
		# if branch_filter and not check_branch_match(row, branch_filter):
		# 	continue

		date = row.get("due_date")
		if date not in date_wise_data:
			date_wise_data[date] = {"income": 0, "expense": 0}

		date_wise_data[date]["income"] += flt(row.get("income", 0))
		date_wise_data[date]["expense"] += flt(row.get("expense", 0))

	dates = sorted(date_wise_data.keys())
	incomes = [date_wise_data[date]["income"] for date in dates]
	expenses = [date_wise_data[date]["expense"] for date in dates]

	return {
		"data": {
			"labels": [formatdate(date) for date in dates],
			"datasets": [
				{"name": _("Income"), "values": incomes},
				{"name": _("Expense"), "values": expenses},
			],
		},
		"type": "line",
		"height": 300,
		"colors": [CHART_COLORS["green"], CHART_COLORS["red"]],
		"axisOptions": {"xIsSeries": True},
	}


def get_balance_trend_chart(data, filters):
	date_wise_data = {}
	# branch_filter = get_filter_list(filters.get("branch")) if filters and filters.get("branch") else None

	for row in data:
		# if branch_filter and not check_branch_match(row, branch_filter):
		# 	continue

		date = row.get("due_date")
		if date not in date_wise_data:
			date_wise_data[date] = {"income": 0, "expense": 0}

		date_wise_data[date]["income"] += flt(row.get("income", 0))
		date_wise_data[date]["expense"] += flt(row.get("expense", 0))

	dates = sorted(date_wise_data.keys())
	running_balance = 0
	balance_values = []

	for date in dates:
		daily_net = date_wise_data[date]["income"] - date_wise_data[date]["expense"]
		running_balance += daily_net
		balance_values.append(running_balance)

	return {
		"data": {
			"labels": [formatdate(date) for date in dates],
			"datasets": [{"name": _("Balance"), "values": balance_values}],
		},
		"type": "line",
		"height": 300,
		"colors": ["#007bff"],
		"axisOptions": {"xIsSeries": True},
	}


def get_income_expense_comparison_chart(data, filters):
	date_wise_data = {}
	# branch_filter = get_filter_list(filters.get("branch")) if filters and filters.get("branch") else None

	for row in data:
		# if branch_filter and not check_branch_match(row, branch_filter):
		# 	continue

		date = row.get("due_date")
		if date not in date_wise_data:
			date_wise_data[date] = {"income": 0, "expense": 0}

		date_wise_data[date]["income"] += flt(row.get("income", 0))
		date_wise_data[date]["expense"] += flt(row.get("expense", 0))

	dates = sorted(date_wise_data.keys())
	incomes = [date_wise_data[date]["income"] for date in dates]
	expenses = [date_wise_data[date]["expense"] for date in dates]

	return {
		"data": {
			"labels": [formatdate(date) for date in dates],
			"datasets": [
				{"name": _("Income"), "values": incomes},
				{"name": _("Expense"), "values": expenses},
			],
		},
		"type": "bar",
		"height": 300,
		"colors": [CHART_COLORS["green"], CHART_COLORS["red"]],
	}


def get_daily_bar_comparison_chart(data, filters):
	date_wise_data = {}
	# branch_filter = get_filter_list(filters.get("branch")) if filters and filters.get("branch") else None

	for row in data:
		# if branch_filter and not check_branch_match(row, branch_filter):
		# 	continue

		date = row.get("due_date")
		if date not in date_wise_data:
			date_wise_data[date] = {"income": 0, "expense": 0, "net": 0}

		date_wise_data[date]["income"] += flt(row.get("income", 0))
		date_wise_data[date]["expense"] += flt(row.get("expense", 0))
		date_wise_data[date]["balance"] = date_wise_data[date]["income"] - date_wise_data[date]["expense"]

	dates = sorted(date_wise_data.keys())
	net_flows = [date_wise_data[date]["balance"] for date in dates]

	return {
		"data": {
			"labels": [formatdate(date) for date in dates],
			"datasets": [{"name": _("Net Cash Flow"), "values": net_flows}],
		},
		"type": "bar",
		"height": 300,
		"colors": ["#17a2b8"],
	}


def get_weekly_summary_chart(data, filters):
	weekly_data = {}
	# branch_filter = get_filter_list(filters.get("branch")) if filters and filters.get("branch") else None

	for row in data:
		# if branch_filter and not check_branch_match(row, branch_filter):
		# 	continue

		print(row)
		date = row.get("due_date")
		if isinstance(date, str):
			date = getdate(date)

		year_week = f"{date.year}-W{date.isocalendar()[1]:02d}"

		if year_week not in weekly_data:
			weekly_data[year_week] = {"income": 0, "expense": 0}

		weekly_data[year_week]["income"] += flt(row.get("income", 0))
		weekly_data[year_week]["expense"] += flt(row.get("expense", 0))

	weeks = sorted(weekly_data.keys())
	weekly_incomes = [weekly_data[week]["income"] for week in weeks]
	weekly_expenses = [weekly_data[week]["expense"] for week in weeks]

	return {
		"data": {
			"labels": weeks,
			"datasets": [
				{"name": _("Weekly Income"), "values": weekly_incomes},
				{"name": _("Weekly Expense"), "values": weekly_expenses},
			],
		},
		"type": "bar",
		"height": 300,
		"colors": [CHART_COLORS["green"], CHART_COLORS["red"]],
	}


def get_current_account_balance(filters, account_numbers):
	accounts = frappe.get_all(
		"Account",
		filters={"account_number": ["in", account_numbers], "company": filters.get("company"), "is_group": 0},
		fields=["name", "account_name", "account_number"],
	)

	total_balance = 0
	for account in accounts:
		balance = get_balance_on(account.name, date=nowdate())
		total_balance += flt(balance)

	return total_balance
