from erpnext.accounts.report.general_ledger import general_ledger

erpnext_get_balance = general_ledger.get_balance
erpnext_get_result_as_list = general_ledger.get_result_as_list

NOT_ASSET_ACCOUNT_TYPES = [3, 4, 5, 6, 7]

# 1,2 là dư nợ cuối = dư nợ đầu kỳ - dư có đầu kỳ (nếu có) + ps nợ - ps có,
# 3,4 dư có cuối kỳ = dư có đầu kỳ - ps nợ + ps có
# 5 6 7 8 luôn luôn ko có dư nợ cuối kỳ
# nó phải kết chuyển đưa vào 911


def get_result_as_list(data, filters):
    if "group_by" in filters and filters["group_by"] != "Group by Account":
        return erpnext_get_result_as_list(data, filters)

    for idx, d in enumerate(data):
        if not d.get("posting_date"):
            balance, _balance_in_account_currency = 0, 0
            try:
                next_idx = idx + 1
                if (
                    next_idx < len(data)
                    and "account" in data[next_idx]
                    and int(data[next_idx]["account"][0]) in NOT_ASSET_ACCOUNT_TYPES
                ):
                    balance = data[idx].get("credit", 0)
                    d["balance"] = balance
                    d["account_currency"] = filters.account_currency

                    continue
            except ValueError:
                pass

        balance = get_balance_vn(d, balance, "debit", "credit")
        d["balance"] = balance

        d["account_currency"] = filters.account_currency

    return data


def get_balance_vn(row, balance, debit_field, credit_field):
    try:
        if "account" not in row:
            return erpnext_get_balance(row, balance, debit_field, credit_field)

        type_of_account = int(row["account"][0])
        if type_of_account in NOT_ASSET_ACCOUNT_TYPES:
            # 3 - 7 => credit - debit
            balance = balance - row.get(debit_field, 0) + row.get(credit_field, 0)
        else:
            # 1 - 2 => debit - credit
            balance = balance + row.get(debit_field, 0) - row.get(credit_field, 0)
    except ValueError:
        return erpnext_get_balance(row, balance, debit_field, credit_field)

    return balance


general_ledger.get_result_as_list = get_result_as_list
