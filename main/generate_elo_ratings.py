from pathlib import Path
import csv
from elo.Elo import Elo

match_folder = './match_data'
rating_folder = './rating_data'

Path(rating_folder).mkdir(parents=True, exist_ok=True)

start_season = 0
end_season = 10

teams_reader = csv.DictReader(open('./teams.csv'))
teams = {row['teamID']: row['teamName'] for row in teams_reader}

fields = ['combined_day', 'season', 'day', 'teamID', 'rating']

for K in range(2, 21):
	eloboard = Elo(k=K)

	for k in teams:
		eloboard.add_player(k)

	combined_day = 0

	rating_data = csv.DictWriter(open(rating_folder + '/ratings_elo_{k}.csv'.format(k=K), 'w'), fields)

	rating_data.writeheader()
	rating_data.writerows([{'combined_day': combined_day,
							'season': 0, 'day': 0,
							'teamID': k, 'rating': v} for k, v in eloboard.ratings.items()])

	for season in range(start_season, end_season+1):
		season_data = csv.DictReader(open(match_folder + '/season_{season}.csv'.format(season=season)))
		day = '1'
		rating_history = {}
		for match in season_data:
			if day != match['day']:
				rating_history[day] = eloboard.ratings.copy()
				day = match['day']

			eloboard.run_game(match['awayTeam'], match['homeTeam'], match['awayScore'], match['homeScore'])

		rating_history[day] = eloboard.ratings.copy()

		for day, ratings in rating_history.items():
			combined_day += 1
			rating_data.writerows([{'combined_day': combined_day,
									'season': season, 'day': day,
									'teamID': k, 'rating': v} for k, v in ratings.items()])
