from pathlib import Path
import requests

data_folder = './raw_daily_data'

Path(data_folder).mkdir(parents=True, exist_ok=True)

game_url = 'https://www.blaseball.com/database/games?day={day}&season={season}'

start_season = 0
end_season = 10

for season in range(start_season, end_season+1):
	season_folder = data_folder + '/season_{season}'
	Path(season_folder.format(season=season)).mkdir(parents=True, exist_ok=True)

	day = 0
	while True:
		day_file = season_folder + '/day_{day:02}.json'
		if Path(day_file.format(season=season, day=day)).is_file():
			print('Already have day {day} of season {season}'.format(day=day+1, season=season+1))
			day += 1
			continue

		resp = requests.get(game_url.format(day=day, season=season))
		if resp.text == '[]':
			break
		with open('./raw_daily_data/season_{season}/day_{day:02}.json'.format(season=season, day=day), 'w') as f:
			f.write(resp.text)
		print('Finished day {} of season {}'.format(day+1, season+1));
		day += 1
