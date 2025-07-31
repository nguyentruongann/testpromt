frappe.provide("inno.sales_invoice");

const DEFAULT_PRINT_SETTINGS = {
	format: "Sales Invoice",
	letterhead: "",
	no_letterhead: 1,
};

inno.sales_invoice.direct_print_with_settings = function (frm) {
	let params = {
		doctype: frm.doctype,
		name: frm.docname,
		format: DEFAULT_PRINT_SETTINGS.format,
		letterhead: DEFAULT_PRINT_SETTINGS.letterhead,
		no_letterhead: DEFAULT_PRINT_SETTINGS.no_letterhead,
		_lang: frappe.boot.lang || "en",
	};

	let url = "/printview?" + new URLSearchParams(params).toString();

	const iframe = document.createElement("iframe");
	iframe.style.display = "none";

	document.body.appendChild(iframe);

	iframe.onload = function () {
		try {
			iframe.contentWindow.print();
			setTimeout(() => {
				document.body.removeChild(iframe);
			}, 300);
		} catch (e) {
			console.error("Print error:", e);
			document.body.removeChild(iframe);
			frappe.show_alert({
				message: __("Print failed. Please try again."),
				indicator: "red",
			});
		}
	};

	iframe.src = url;

	frappe.show_alert({
		message: __("Printing with default settings..."),
		indicator: "green",
	});
};
