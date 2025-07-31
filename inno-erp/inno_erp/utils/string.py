from slugify import slugify


def scrub(text, **kwargs):
	"""
	Custom slugify function that uses a hyphen as the separator.
	"""
	return slugify(text, **kwargs).upper()
