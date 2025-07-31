import frappe
from erpnext.accounts.doctype.pos_invoice.pos_invoice import POSInvoice
from frappe.utils import add_days, cint, flt, getdate, nowdate
from inno_erp.inno_account.overrides.loyalty_program.loyalty_program import (
    get_loyalty_program_details_with_points,
    update_customer_rank,
)


class InnoPOSInvoice(POSInvoice):
    def make_loyalty_point_entry(self):
        date_of_birth = frappe.get_value(
            "Customer", self.customer, "custom_date_of_birth"
        )
        returned_amount = self.get_returned_amount()
        current_amount = flt(self.grand_total) - cint(self.loyalty_amount)
        eligible_amount = current_amount - returned_amount
        now_date = getdate(nowdate())

        lp_details = get_loyalty_program_details_with_points(
            self.customer,
            company=self.company,
            current_transaction_amount=current_amount,
            loyalty_program=self.loyalty_program,
            expiry_date=self.posting_date,
            include_expired_entry=True,
        )

        if (
            lp_details
            and getdate(lp_details.from_date) <= getdate(self.posting_date)
            and (
                not lp_details.to_date
                or getdate(lp_details.to_date) >= getdate(self.posting_date)
            )
        ):
            collection_factor = (
                lp_details.collection_factor if lp_details.collection_factor else 1.0
            )
            if lp_details.collection_factor:
                date_now = getdate(self.posting_date)
                special_days = lp_details.custom_special_days
                multiplier_rule = 1.0
                for special_day in special_days:
                    if special_day["active"] == 1 and special_day["day_name"]:
                        if special_day["day_name"] == "Birthdate":
                            if date_of_birth:
                                if (
                                    date_of_birth.day == now_date.day
                                    and date_of_birth.month == now_date.month
                                ):
                                    multiplier_rule *= special_day["rate"]

                        date_of_effect = special_day["date"]
                        if date_now == date_of_effect:
                            multiplier_rule *= special_day["rate"]

            points_earned = cint(eligible_amount / collection_factor * multiplier_rule)

            doc = frappe.get_doc(
                {
                    "doctype": "Loyalty Point Entry",
                    "company": self.company,
                    "loyalty_program": lp_details.loyalty_program,
                    "loyalty_program_tier": lp_details.tier_name,
                    "customer": self.customer,
                    "invoice_type": self.doctype,
                    "invoice": self.name,
                    "loyalty_points": points_earned,
                    "purchase_amount": eligible_amount,
                    "expiry_date": add_days(
                        self.posting_date, lp_details.expiry_duration
                    ),
                    "posting_date": self.posting_date,
                }
            )
            doc.flags.ignore_permissions = 1
            doc.save()
            self.set_loyalty_program_tier()
            update_customer_rank(self.customer)

    def set_loyalty_program_tier(self):
        lp_details = get_loyalty_program_details_with_points(
            self.customer,
            company=self.company,
            loyalty_program=self.loyalty_program,
            include_expired_entry=True,
        )
        frappe.db.set_value(
            "Customer", self.customer, "loyalty_program_tier", lp_details.tier_name
        )
