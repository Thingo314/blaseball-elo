from pathlib import Path
import requests
import json
import csv

match_folder = './match_data'
data_folder = './raw_daily_data'

Path(match_folder).mkdir(parents=True, exist_ok=True)

start_season = 0
end_season = 10

fields = ['day', 'awayTeam', 'homeTeam', 'isPostseason', 'awayScore', 'homeScore']

teams = {}

for season in range(start_season, end_season+1):
	data_file = data_folder + '/season_{season}/day_{day:02}.json'
	day = 0

	season_data = csv.DictWriter(open(match_folder + '/season_{season}.csv'.format(season=season), 'w'), fields)
	season_data.writeheader()

	while Path(data_file.format(season=season, day=day)).is_file():
		with open(data_file.format(season=season, day=day)) as f:
			data = json.load(f)

		for match in data:
			row = {}
			for field in fields:
				row[field] = match[field]

			row['day'] += 1
			season_data.writerow(row)

			teams[match['awayTeam']] = match['awayTeamName']
			teams[match['homeTeam']] = match['homeTeamName']

		day += 1

teams_data = csv.DictWriter(open('./teams.csv', 'w'), ['teamID', 'teamName'])

teams_data.writeheader()
teams_data.writerows([{'teamID': k, 'teamName':v} for k,v in teams.items()])
