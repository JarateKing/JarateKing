def queryString(start=2015, end=2020):
	ret = "query {\n\t viewer {\n"
	for year in range(start, end + 1):
		ret = ret + "\t\tq" + str(year) + ": contributionsCollection(from: \"" + str(year) + "-01-01T00:00:00.000+00:00\") { contributionCalendar { weeks { contributionDays { date contributionCount } } } }\n"
	
	ret = ret + "\t}\n}"
	return ret

print(queryString())