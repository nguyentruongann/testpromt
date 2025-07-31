ADDRESS_LOCATION_SPLITTER = " - "
ADDRESS_WARD_SPLITTER = "-"


def format_location(location):
	location = location.split(ADDRESS_LOCATION_SPLITTER)
	return location[0], location[1]


def format_ward(wardname):
	return wardname.split(ADDRESS_WARD_SPLITTER)[0]
