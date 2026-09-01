from python_graphql_client import GraphqlClient
import json
import os
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

# setup graphql client 
client = GraphqlClient(endpoint="https://api.github.com/graphql")
oauth_token = os.environ.get("JARATEKING_TOKEN", "")

# setup api query
def queryString(start=2015, end=2026):
	ret = "query {\n\t viewer {\n"
	for year in range(start, end + 1):
		ret = ret + "\t\tq" + str(year) + ": contributionsCollection(from: \"" + str(year) + "-01-01T00:00:00.000+00:00\") { contributionCalendar { weeks { contributionDays { date contributionCount } } } }\n"
	
	ret = ret + "\t}\n}"
	return ret

# parse api and get longest streak
def longestStreak(data):
	startDate = "1960-01-01T00:00:00.000+00:00"
	endDate = "1960-01-01T00:00:00.000+00:00"
	streak = 0
	currentStreak = False
	for year in data["data"]["viewer"]:
		for week in data["data"]["viewer"][year]["contributionCalendar"]["weeks"]:
			for day in week["contributionDays"]:
				if (day["date"][0:4] == year[1:5]):
					if (day["contributionCount"] > 0):
						if (currentStreak):
							streak = streak + 1
							endDate = day["date"]
						else:
							streak = 1
							startDate = day["date"]
							endDate = startDate
							currentStreak = True
					else:
						currentStreak = False
	return streak, startDate, endDate

def humanReadableDiff(startDate, endDate):
	start = parser.parse(startDate)
	end = parser.parse(endDate)
	diff = relativedelta(end, start)
	
	yearstr = "{} year{}".format(diff.years, "" if diff.years == 1 else "s")
	monthstr = "{} month{}".format(diff.months, "" if diff.months == 1 else "s")
	daystr = "{} day{}".format(diff.days, "" if diff.days == 1 else "s")
	
	if (diff.years > 0):
		return "{}, {}, {}".format(yearstr, monthstr, daystr)
	elif (diff.months > 0):
		return "{}, {}".format(monthstr, daystr)
	else:
		return "{}".format(daystr)

# main
json_data = client.execute(query=queryString(), headers={"Authorization": "Bearer {}".format(oauth_token)})
streak, startDate, endDate = longestStreak(json_data)
diff = humanReadableDiff(startDate, endDate)
readme = open('README.md', 'w')

prefix = open('prefix.md', 'r')
readme.write(prefix.read())
readme.write("Daily Contributions Streak: **" + str(streak) + "** (" + diff + " / " + startDate[0:10] + " to " + endDate[0:10] + ")")
suffix = open('suffix.md', 'r')
readme.write(suffix.read())
