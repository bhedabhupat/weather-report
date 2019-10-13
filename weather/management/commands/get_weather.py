from django.core.management.base import BaseCommand, CommandError
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('place', type=str)
		parser.add_argument('type', type=str, nargs='?', default='today')

	def handle(self, *args, **options):
		place = options['place']
		ftype = options['type']
		available_types = ['today','hourbyhour','5day','tenday']
		if not ftype in available_types:
			ftype = 'today'
		try:
			get_place = requests.get("https://api.weather.com/v3/location/search?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&language=en-US&locationType=locale&query="+str(place))
			placeId = get_place.json()['location']['placeId'][0]
			page = requests.get("https://weather.com/en-IN/weather/"+str(ftype)+"/l/"+str(placeId))
			soup = BeautifulSoup(page.content, 'html.parser')
			if ftype == 'today':
				title_span = soup.select('span.today_nowcard-loc-title-wrqpper')[0]
				print(title_span.select("h1.today_nowcard-location")[0].get_text())
				maindiv = soup.find(class_="today_nowcard-sidecar component panel")
				innerdiv = soup.select('table')[0]
				datath = innerdiv.find_all('tr')
				for th in list(datath):
					print(th.get_text())
					# datatd = innerdiv.select("td")
			else:
				titlediv = soup.find(class_="locations-title")
				print(titlediv.select('h1')[0].get_text())
				maindiv = soup.find(id="main-DailyForecast-1c4c02b8-a3fd-4069-b54e-93db18c89c1b")
				innerdiv = soup.find(class_='twc-table')
				datath = innerdiv.select('th')
				for th in list(datath):
					print(th.get_text())
				datatd = innerdiv.select("td")
				for td in list(datatd):
					print(td.get_text())

		except Exception as e:
			print(str(e))
		