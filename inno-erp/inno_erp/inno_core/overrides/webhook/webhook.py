import json
from time import sleep

import frappe
import requests
from frappe.integrations.doctype.webhook import webhook
from frappe.integrations.doctype.webhook.webhook import (
	WEBHOOK_SECRET_HEADER,
	Webhook,
	get_context,
	get_webhook_data,
	get_webhook_headers,
	log_request,
)

INNO_WEBHOOK_SECRET_HEADER = "X-Tada-Webhook-Signature"


def inno_enqueue_webhook(doc, webhook) -> None:
	request_url = headers = data = r = None
	try:
		webhook: Webhook = frappe.get_doc("Webhook", webhook.get("name"))
		request_url = webhook.request_url
		if webhook.is_dynamic_url:
			request_url = frappe.render_template(webhook.request_url, get_context(doc))
		headers = get_webhook_headers(doc, webhook)
		### Replace key headers to Tada-Webhook-Signature
		if WEBHOOK_SECRET_HEADER in headers:
			headers[INNO_WEBHOOK_SECRET_HEADER] = headers.pop(WEBHOOK_SECRET_HEADER)
		### END CUSTOMIZATION
		data = get_webhook_data(doc, webhook)

	except Exception as e:
		frappe.logger().debug({"enqueue_webhook_error": e})
		log_request(webhook.name, doc.name, request_url, headers, data)
		return

	for i in range(3):
		try:
			r = requests.request(
				method=webhook.request_method,
				url=request_url,
				data=json.dumps(data, default=str),
				headers=headers,
				timeout=webhook.timeout or 5,
			)
			r.raise_for_status()
			frappe.logger().debug({"webhook_success": r.text})
			log_request(webhook.name, doc.name, request_url, headers, data, r)
			break

		except requests.exceptions.ReadTimeout as e:
			frappe.logger().debug({"webhook_error": e, "try": i + 1})
			log_request(webhook.name, doc.name, request_url, headers, data)

		except Exception as e:
			frappe.logger().debug({"webhook_error": e, "try": i + 1})
			log_request(webhook.name, doc.name, request_url, headers, data, r)
			sleep(3 * i + 1)
			if i != 2:
				continue


webhook.enqueue_webhook = inno_enqueue_webhook
