from python_graphql_client import GraphqlClient
import json

client = GraphqlClient(endpoint="https://api.github.com/graphql")
oauth_token = os.environ.get("JARATEKING_TOKEN", "")

def queryString(start=2015, end=2020):
	ret = "query {\n\t viewer {\n"
	for year in range(start, end + 1):
		ret = ret + "\t\tq" + str(year) + ": contributionsCollection(from: \"" + str(year) + "-01-01T00:00:00.000+00:00\") { contributionCalendar { weeks { contributionDays { date contributionCount } } } }\n"
	
	ret = ret + "\t}\n}"
	return ret
	
def longestStreak(data):
	startDate = "1960-01-01T00:00:00.000+00:00"
	endDate = "1960-01-01T00:00:00.000+00:00"
	streak = 0
	currentStreak = False
	for year in data["data"]["viewer"]:
		for week in data["data"]["viewer"][year]["contributionCalendar"]["weeks"]:
			for day in week["contributionDays"]:
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

json_data = client.execute(query=queryString(), headers={"Authorization": "Bearer {}".format(oauth_token)})
data = json.load(json_data)
streak, startDate, endDate  = longestStreak(data)
readme = open('README.md', 'w')
readme.write("Daily Contributions Streak: **" + str(streak) + "** (" + startDate[0:10] + " to " + endDate[0:10] + ")")
	