import frappe
from frappe import _, utils
from frappe.utils import money_in_words as money_in_words_frappe


#
# convert currency to words
#
def money_in_words(
	number: str | float | int,
	main_currency: str | None = None,
	fraction_currency: str | None = None,
):
	result = money_in_words_frappe(number, main_currency, fraction_currency)
	locale = frappe.local.lang or "vi"

	need_to_remove = _("only.")
	if locale == "vi" and need_to_remove in result:
		result = result.replace(need_to_remove, "")
	return result


utils.money_in_words = money_in_words
