frappe.provide("frappe.search");
import slugify from "slugify";
import { fuzzy_match } from "frappe/public/js/frappe/ui/toolbar/fuzzy_match.js";

const SLUGIFY_OPTIONS = {
	lower: true,
	strict: true,
	locale: "vi",
	trim: true,
};

Object.assign(frappe.search.utils, {
	fuzzy_search: function inno_fuzzy_search(
		keywords = "",
		_item = "",
		return_marked_string = false,
	) {
		const item = __(_item);

		const [, score, matches] = fuzzy_match(
			slugify(keywords, SLUGIFY_OPTIONS),
			slugify(item, SLUGIFY_OPTIONS),
			return_marked_string,
		);

		if (!return_marked_string) {
			return score;
		}
		if (score === 0) {
			return {
				score: score,
				marked_string: item,
			};
		}

		// Create Boolean mask to mark matching indices in the item string
		const matchArray = Array(item.length).fill(0);
		for (const index of matches) {
			matchArray[index] = 1;
		}

		let marked_string = "";
		let buffer = "";

		// Clear the buffer and return marked matches.
		const flushBuffer = () => {
			if (!buffer) return "";
			const temp = `<mark>${buffer}</mark>`;
			buffer = "";
			return temp;
		};

		matchArray.forEach((isMatch, index) => {
			if (isMatch) {
				buffer += item[index];
			} else {
				marked_string += flushBuffer();
				marked_string += item[index];
			}
		});
		marked_string += flushBuffer();

		return { score, marked_string };
	},
});
