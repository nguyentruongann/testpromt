from frappe import _


def get():
	return {
		_("Short-term Assets"): {
			_("Cash On Hand"): {
				_("Vietnamese Dong"): {
					"account_number": "1111",
					"account_type": "Cash",
				},
				_("Foreign Currencies"): {
					"account_number": "1112",
				},
				_("Monetary Gold"): {
					"account_number": "1113",
				},
				"account_number": "111",
				"account_type": "Cash",
			},
			_("Cash In Banks"): {
				_("Vietnamese Dong"): {
					"account_number": "1121",
					"account_type": "Bank",
				},
				_("Foreign Currencies"): {
					"account_number": "1122",
				},
				_("Monetary Gold"): {
					"account_number": "1123",
				},
				"account_type": "Bank",
				"account_number": "112",
			},
			_("Cash In Transit"): {
				_("Vietnamese Dong"): {
					"account_number": "1131",
					"account_type": "Temporary",
				},
				_("Foreign Currencies"): {
					"account_number": "1132",
				},
				"account_number": "113",
			},
			_("Trading Securities"): {
				_("Shares"): {
					"account_number": "1211",
				},
				_("Bonds"): {
					"account_number": "1212",
				},
				_("Securities And Other Financial Instruments"): {
					"account_number": "1218",
				},
				"account_number": "121",
			},
			_("Investments Held To Maturity"): {
				_("Time Deposits"): {
					"account_number": "1281",
				},
				_("Bonds"): {
					"account_number": "1282",
				},
				_("Loan"): {
					"account_number": "1283",
				},
				_("Other Investments Held To Maturity"): {"account_number": "1288"},
				"account_number": "128",
			},
			_("Trade Receivables"): {
				"account_type": "Receivable",
				"account_number": "131",
			},
			_("Deductible VAT"): {
				_("Deductible VAT Of Goods And Services"): {
					"account_number": "1331",
				},
				_("Deductible VAT Of Fixed Assets"): {"account_number": "1332"},
				"account_number": "133",
			},
			_("Internal Receivables"): {
				_("Working Capital Provided To Sub-units"): {
					"account_number": "1361",
				},
				_("Internal Receivables On Foreign Exchange Diff"): {"account_number": "1362"},
				_("Internal Receivables On Borrowing Cost Eligible For Capitalization"): {
					"account_number": "1363"
				},
				_("Other Internal Receivables"): {
					"account_number": "1368",
				},
				"account_number": "136",
			},
			_("Other Receivables"): {
				_("Shortage Of Assets Awaiting Resolution"): {"account_number": "1381"},
				_("Privatization Receivables"): {"account_number": "1385"},
				_("Other Receivables"): {"account_number": "1388"},
				"account_number": "138",
			},
			_("Advances"): {
				"account_number": "141",
			},
			_("Goods In Transit"): {
				"account_number": "151",
			},
			_("Raw Materials"): {
				"account_number": "152",
			},
			_("Tools & Supplies"): {
				_("Tools & Supplies"): {
					"account_number": "1531",
				},
				_("Packaging Rotation"): {
					"account_number": "1532",
				},
				_("Instrument For Rent"): {
					"account_number": "1533",
				},
				_("Equipment & Spare Parts"): {
					"account_number": "1534",
				},
				"account_number": "153",
			},
			_("Work In Process"): {
				"account_number": "154",
			},
			_("Finished Products"): {
				_("Finished Products"): {
					"account_number": "1551",
				},
				_("Real Estate Finished Goods"): {"account_number": "1557"},
				"account_number": "155",
			},
			_("Merchandise Goods"): {
				_("Purchase Costs"): {
					"account_number": "1561",
					"account_type": "Stock",
				},
				_("Incidental Expense"): {
					"account_number": "1562",
					"account_type": "Expenses Included In Valuation",
				},
				_("Property Inventories"): {
					"account_number": "1567",
				},
				"account_number": "156",
			},
			_("Outward Goods On Consignment"): {"account_number": "157"},
			_("Goods In Bonded Warehouse"): {
				"account_number": "158",
			},
			_("Government Source Expenditure"): {
				_("Previous Years Expenditure"): {"account_number": "1611"},
				_("Current Years Expenditure"): {
					"account_number": "1612",
				},
				"account_number": "161",
			},
			_("Government Bonds Purchase-resale"): {"account_number": "171"},
			"root_type": "Asset",
			"account_number": "1",
		},
		_("Long-term Assets"): {
			_("Tangible Fixed Assets"): {
				_("Building & Structures"): {
					"account_number": "2111",
					"account_type": "Fixed Asset",
				},
				_("Machinery & Equipment"): {
					"account_number": "2112",
					"account_type": "Fixed Asset",
				},
				_("Transportation & Transmission Vehicles"): {
					"account_number": "2113",
					"account_type": "Fixed Asset",
				},
				_("Office Equipment"): {
					"account_number": "2114",
					"account_type": "Fixed Asset",
				},
				_("Perennial Trees, Working And Producing Animals"): {"account_number": "2115"},
				_("Other Tangible Fixed Assets"): {"account_number": "2118"},
				"account_number": "211",
			},
			_("Financial Leased Assets"): {
				_("Financial Leased Tangible Assets"): {
					"account_number": "2121",
				},
				_("Financial Leased Intangible Assets"): {
					"account_number": "2122",
				},
				"account_number": "212",
			},
			_("Intangible Fixed Assets"): {
				_("Land Use Right"): {
					"account_number": "2131",
				},
				_("Copyrights"): {
					"account_number": "2132",
				},
				_("Patents"): {
					"account_number": "2133",
				},
				_("Trademarks And Brand Name"): {"account_number": "2134"},
				_("Computer Software"): {"account_number": "2135"},
				_("License & Franchises"): {
					"account_number": "2136",
				},
				_("Other Intangible Fixed Assets"): {
					"account_number": "2138",
				},
				"account_number": "213",
			},
			_("Depreciation Of Fixed Assets"): {
				_("Depreciation Of Tangible Fixed Assets"): {
					"account_number": "2141",
					"account_type": "Accumulated Depreciation",
				},
				_("Depreciation Of Financial Leased Assets"): {
					"account_number": "2142",
				},
				_("Depreciation Of Intangible Fixed Assets"): {
					"account_number": "2143",
				},
				_("Depreciation Of Investment Properties"): {
					"account_number": "2147",
				},
				"account_number": "214",
			},
			_("Investment Properties"): {
				"account_number": "217",
			},
			_("Investment In Subsidiaries"): {"account_number": "221"},
			_("Investment In Joint Venture And Associates"): {"account_number": "222"},
			_("Other Investments"): {
				_("Equity Investment In Other Entity"): {"account_number": "2281"},
				_("Other Investment"): {"account_number": "2288"},
				"account_number": "228",
			},
			_("Allowance For Impairment Of Assets"): {
				_("Allowance For Decline In Value Of Trading Securities"): {
					"account_number": "2291",
				},
				_("Allowance For Investment Loss In Other Entity"): {"account_number": "2292"},
				_("Allowance For Doubtful Debt"): {"account_number": "2293"},
				_("Inventory Reserve"): {"account_number": "2294"},
				"account_number": "229",
			},
			_("Construction In Progress"): {
				_("Acquisition Of Fixed Assets"): {
					"account_number": "2411",
				},
				_("Construction In Progress"): {
					"account_number": "2412",
					"account_type": "Expenses Included In Asset Valuation",
				},
				_("Extra-Ordinary Repair Of Fixed Assets"): {
					"account_number": "2413",
				},
				"account_number": "241",
				"account_type": "Capital Work in Progress",
			},
			_("Prepaid Expenses"): {"account_number": "242"},
			_("Deferred Tax Assets"): {"account_number": "243"},
			_("Mortgage, Collaterals And Deposits"): {
				"account_number": "244",
			},
			"root_type": "Asset",
			"account_number": "2",
		},
		_("Liabilities"): {
			_("Trade Payables"): {"account_number": "331", "account_type": "Payable"},
			_("Taxes And Other Payable To State Budget"): {
				_("Value Added Tax (VAT)"): {
					_("VAT Output"): {"account_number": "33311"},
					_("VAT On Imported Goods"): {"account_number": "33312"},
					"account_number": "3331",
				},
				_("Special Consumption Tax"): {"account_number": "3332"},
				_("Import & Export Duties"): {"account_number": "3333"},
				_("Corporate Income Tax"): {"account_number": "3334"},
				_("Personal Income Tax"): {"account_number": "3335"},
				_("Natural Resources Using Tax"): {"account_number": "3336"},
				_("Land & Housing Tax, Land Rental Charges"): {"account_number": "3337"},
				_("Environment Protection Tax And Other Taxes"): {
					"account_number": "3338",
					_("Environment Protection Tax"): {"account_number": "33381"},
					_("Other Taxes"): {"account_number": "33382"},
				},
				_("Fee & Charge & Other Payables"): {"account_number": "3339"},
				"account_number": "333",
				"account_type": "Tax",
			},
			_("Payable To Employees"): {
				_("Payable To Employees"): {"account_number": "3341"},
				_("Payable To Other"): {"account_number": "3348"},
				"account_number": "334",
			},
			_("Accrued Expenses"): {
				"account_number": "335",
				"account_type": "Asset Received But Not Billed",
			},
			_("Internal Payables"): {
				_("Internal Payables For Working Capital Received"): {
					"account_number": "3361",
				},
				_("Internal Payables For Foreign Exchange Diff"): {
					"account_number": "3362",
				},
				_("Internal Payables For Borrowing Cost Eligible For Capitalization"): {
					"account_number": "3363"
				},
				_("Other Internal Payables"): {"account_number": "3368"},
				"account_number": "336",
			},
			_("Progress Billings For Contruction Contract"): {"account_number": "337"},
			_("Other Payables"): {
				_("Surplus Of Assets Awaiting For Resolution"): {"account_number": "3381"},
				_("Trade Union Fees"): {"account_number": "3382"},
				_("Social Insurance"): {"account_number": "3383"},
				_("Health Insurance"): {"account_number": "3384"},
				_("Privatization Payable"): {"account_number": "3385"},
				_("Unemployment Insurance"): {"account_number": "3386"},
				_("Unearned Revenue"): {"account_number": "3387"},
				_("Others"): {"account_number": "3388"},
				"account_number": "338",
			},
			_("Borrowings And Finance Lease Liabilities"): {
				_("Borrowings"): {"account_number": "3411"},
				_("Finance Lease Liabilities"): {
					"account_number": "3412",
				},
				"account_number": "341",
			},
			_("Issued Bonds"): {
				_("Ordinary Bonds"): {
					"account_number": "3431",
					_("Par Value Of Bonds"): {
						"account_number": "34311",
					},
					_("Bond Discounts"): {
						"account_number": "34312",
					},
					_("Bond Premiums"): {
						"account_number": "34313",
					},
				},
				_("Convertible Bonds"): {"account_number": "3432"},
				"account_number": "343",
			},
			_("Deposits Received"): {"account_number": "344"},
			_("Deferred Tax Liabilities"): {"account_number": "347"},
			_("Provisions Payables"): {
				_("Product Warranty Provisions"): {"account_number": "3521"},
				_("Construction Warranty Provisions"): {"account_number": "3522"},
				_("Enterprise Restructuring Provisions"): {
					"account_number": "3523",
				},
				_("Other Provisions"): {
					"account_number": "3524",
				},
				"account_number": "352",
			},
			_("Bonus And Welfare Fund"): {
				_("Bonus Fund"): {
					"account_number": "3531",
				},
				_("Welfare Fund"): {
					"account_number": "3532",
				},
				_("Welfare Fund Used For Fixed Asset Acquisitions"): {"account_number": "3533"},
				_("Management Bonus Fund"): {
					"account_number": "3534",
				},
				"account_number": "353",
			},
			_("Science And Technology Development Fund"): {
				_("Science And Technology Development Fund"): {
					"account_number": "3561",
				},
				_("Science And Technology Development Fund Used For Fixed Asset Acquisition"): {
					"account_number": "3562",
				},
				"account_number": "356",
			},
			_("Price Stabilization Fund"): {"account_number": "357"},
			"root_type": "Liability",
			"account_number": "3",
		},
		_("Equity"): {
			_("Owner's Equity"): {
				_("Contributed Capital"): {
					_("Ordinary Shares With Voting Rights"): {
						"account_number": "41111",
					},
					_("Preference Shares"): {
						"account_number": "41112",
					},
					"account_type": "Equity",
					"account_number": "4111",
				},
				_("Capital Surplus"): {
					"account_number": "4112",
				},
				_("Conversion Options On Convertible Bonds"): {
					"account_number": "4113",
				},
				_("Other Capital"): {
					"account_number": "4118",
				},
				"account_type": "Equity",
				"account_number": "411",
			},
			_("Revaluation Differences On Asset"): {
				"account_number": "412",
			},
			_("Foreign Exchange Differences"): {
				"account_number": "413",
				_(
					"Exchange Rate Differences On Revaluation Of Monetary Items Denominated In Foreign Currency"
				): {
					"account_number": "4131",
				},
				_("Exchange Rate Differences In Preoperating Period"): {
					"account_number": "4132",
				},
			},
			_("Investment & Development Funds"): {
				"account_number": "414",
			},
			_("Enterprise Reorganization Assistance Fund"): {
				"account_number": "417",
			},
			_("Other Equity Funds"): {
				"account_number": "418",
			},
			_("Treasury Stocks"): {
				"account_number": "419",
			},
			_("Undistributed Profit After Tax"): {
				_("Undistributed Profit After Tax Of Previous Year"): {
					"account_number": "4211",
				},
				_("Undistributed Profit After Tax Of Current Year"): {"account_number": "4212"},
				"account_number": "421",
			},
			_("Capital Expenditure Funds"): {
				"account_number": "441",
			},
			_("Government Sourced Funds"): {
				_("Government Sourced Funds Of Previous Year"): {"account_number": "4611"},
				_("Government Sourced Funds Of Current Year"): {"account_number": "4612"},
				"account_number": "461",
			},
			_("Non-Business Funds Used For Fixed Asset Acquisitions"): {"account_number": "466"},
			"root_type": "Equity",
			"account_number": "4",
		},
		_("Revenue"): {
			_("Revenues"): {
				_("Revenue From Sales Of Merchandises"): {
					"account_number": "5111",
					"account_type": "Income Account",
				},
				_("Revenue From Sales Of Finished Goods"): {
					"account_number": "5112",
				},
				_("Revenue From Services Rendered"): {
					"account_number": "5113",
				},
				_("Revenue From Government Grants"): {
					"account_number": "5114",
				},
				_("Revenue From Investment Properties"): {"account_number": "5117"},
				_("Other Revenue"): {"account_number": "5118"},
				"account_number": "511",
			},
			_("Financial Income"): {"account_number": "515"},
			_("Revenue Deductions"): {
				_("Sales Discounts"): {
					"account_number": "5211",
				},
				_("Sales Allowances"): {
					"account_number": "5212",
				},
				_("Sales Returns"): {"account_number": "5213"},
				"account_number": "521",
			},
			"root_type": "Income",
			"account_number": "5",
		},
		_("Production Costs"): {
			_("Purchases"): {
				_("Raw Material Purchases"): {"account_number": "6111"},
				_("Goods Purchases"): {
					"account_number": "6112",
					"account_type": "Stock Adjustment",
				},
				"account_number": "611",
			},
			_("Direct Raw Materials Costs"): {
				"account_number": "621",
			},
			_("Direct Labor Costs"): {
				"account_number": "622",
			},
			_("Costs Of Construction Machinery"): {
				_("Labor Cost"): {
					"account_number": "6231",
				},
				_("Material Cost"): {
					"account_number": "6232",
				},
				_("Tools And Instruments"): {"account_number": "6233"},
				_("Depreciation Expense"): {
					"account_number": "6234",
				},
				_("Outside Services"): {
					"account_number": "6237",
				},
				_("Other Expenses"): {
					"account_number": "6238",
				},
				"account_number": "623",
			},
			_("Production Overheads"): {
				_("Factory Staff Costs"): {"account_number": "6271"},
				_("Material Cost"): {
					"account_number": "6272",
				},
				_("Tools And Instruments"): {
					"account_number": "6273",
				},
				_("Fixed Asset Depreciation"): {
					"account_number": "6274",
					"account_type": "Depreciation",
				},
				_("Outside Services"): {
					"account_number": "6277",
				},
				_("Other Expenses"): {"account_number": "6278"},
				"account_number": "627",
			},
			_("Production Costs"): {"account_number": "631"},
			_("Costs Of Goods Sold"): {
				"account_number": "632",
				"account_type": "Cost of Goods Sold",
			},
			_("Financial Expenses"): {"account_number": "635"},
			_("Selling Expenses"): {
				_("Employees Costs"): {"account_number": "6411"},
				_("Materials And Packing Materials"): {"account_number": "6412"},
				_("Tools And Instruments"): {"account_number": "6413"},
				_("Fixed Asset Depreciation"): {"account_number": "6414"},
				_("Warranty Expenses"): {"account_number": "6415"},
				_("Outside Services"): {
					"account_number": "6417",
				},
				_("Other Costs"): {"account_number": "6418"},
				"account_number": "641",
			},
			_("General & Administration Expenses"): {
				_("Employees Cost"): {"account_number": "6421"},
				_("Office Supply Expenses"): {"account_number": "6422"},
				_("Stationery Cost"): {"account_number": "6423"},
				_("Fixed Asset Depreciation"): {"account_number": "6424"},
				_("Taxes, Fees, Charges"): {
					"account_number": "6425",
				},
				_("Provision Expenses"): {
					"account_number": "6426",
				},
				_("Outside Services"): {"account_number": "6427"},
				_("Other Costs"): {
					"account_number": "6428",
				},
				"account_number": "642",
			},
			"root_type": "Expense",
			"account_number": "6",
		},
		_("Other Income"): {
			_("Other Income"): {
				"account_number": "711",
			},
			"root_type": "Income",
			"account_number": "7",
		},
		_("Other Expenses"): {
			_("Other Expenses"): {"account_number": "811", "account_type": "Round Off"},
			_("Income Tax Expenses"): {
				_("Current Tax Expenses "): {
					"account_number": "8211",
				},
				_("Deferred Tax Expenses"): {
					"account_number": "8212",
				},
				"account_number": "821",
			},
			"root_type": "Expense",
			"account_number": "8",
		},
		_("Income Summary"): {
			_("Income Summary"): {
				"account_number": "911",
			},
			"root_type": "Income",
			"account_number": "9",
		},
	}
