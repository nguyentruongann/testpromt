// Copyright (c) 2025, Tada Labs and contributors
// For license information, please see license.txt

const PREFIX_SERVICE_PROVIDERS = ["ghtk", "ghn", "viettel"];
const SUFFIX_ENABLE = "_enable";
const QUERY_PROVIDERS = [
	{
		key: "ghtk_pickup_warehouses",
		provider: "GHTK",
	},
	{
		key: "ghn_pickup_warehouses",
		provider: "GHN",
	},
	{
		key: "viettel_pickup_warehouses",
		provider: "ViettelPost",
	},
];

frappe.ui.form.on("Delivery Setting", {
	refresh(frm) {
		refresh_delivery_setting(frm);
		frm.trigger("set_query_for_providers");
	},
	set_query_for_providers(frm) {
		for (const prov of QUERY_PROVIDERS) {
			frm.set_query("pickup_address", prov.key, () => {
				return {
					filters: {
						provider: prov.provider,
					},
				};
			});
		}
	},
	validate(frm) {
		const ghtk_pickups = frm.doc.ghtk_pickup_warehouses.map((pickup) => pickup.warehouse);
		const ghtk_pickups_set = new Set(ghtk_pickups);
		if (ghtk_pickups.length !== ghtk_pickups_set.size) {
			frappe.throw(__("Pickup Warehouse of GHTK must be unique"));
		}

		const ghn_pickups = frm.doc.ghn_pickup_warehouses.map((pickup) => pickup.warehouse);
		const ghn_pickups_set = new Set(ghn_pickups);
		if (ghn_pickups.length !== ghn_pickups_set.size) {
			frappe.throw(__("Pickup Warehouse of GHN must be unique"));
		}

		const viettel_pickups = frm.doc.viettel_pickup_warehouses.map(
			(pickup) => pickup.warehouse
		);
		const viettel_pickups_set = new Set(viettel_pickups);
		if (viettel_pickups.length !== viettel_pickups_set.size) {
			frappe.throw(__("Pickup Warehouse of ViettelPost must be unique"));
		}
	},
	ghtk_sync(frm) {
		frm.call({
			method: "inno_erp.inno_stock.doctype.pickup_address.pickup_address.sync_pickup_address_ghtk",
			freeze: true,
			freeze_message: __("Syncing Pickups..."),
			callback: (r) => {
				frappe.msgprint(__("Synced Pickup Addresses Successfully"));
			},
		});
	},
	ghtk_enable(frm) {
		refresh_delivery_setting(frm, "ghtk");
	},
	ghn_sync(frm) {
		frm.call({
			method: "inno_erp.inno_stock.doctype.pickup_address.pickup_address.sync_pickup_address_ghn",
			freeze: true,
			freeze_message: __("Syncing Pickups..."),
			callback: (r) => {
				frappe.msgprint(__("Synced Pickup Addresses Successfully"));
			},
		});
	},
	ghn_enable(frm) {
		refresh_delivery_setting(frm, "ghn");
	},
	viettel_enable(frm) {
		refresh_delivery_setting(frm, "viettel");
	},
	viettel_sync(frm) {
		frm.call({
			method: "inno_erp.inno_stock.doctype.pickup_address.pickup_address.sync_pickup_address_viettel",
			freeze: true,
			freeze_message: __("Syncing Pickups..."),
			callback: (r) => {
				frappe.msgprint(__("Synced Pickup Addresses Successfully"));
			},
		});
	},
});

function refresh_delivery_setting(frm, change_provider) {
	const doc = frm.doc;
	const providers = !change_provider ? PREFIX_SERVICE_PROVIDERS : [change_provider];

	for (const provider of providers) {
		const prefix = provider + "_";
		for (const key in doc) {
			if (key.startsWith(prefix)) {
				if (key.endsWith(SUFFIX_ENABLE)) continue;
				frm.set_df_property(key, "read_only", !doc[provider + SUFFIX_ENABLE]);
				frm.set_df_property(key, "hidden", !doc[provider + SUFFIX_ENABLE]);
			}
		}
		frm.set_df_property(`${prefix}token`, "read_only", !doc[provider + SUFFIX_ENABLE]);
		frm.set_df_property(`${prefix}token`, "hidden", !doc[provider + SUFFIX_ENABLE]);
		frm.set_df_property(`${prefix}token`, "enable_password_checks", false);
	}
}
