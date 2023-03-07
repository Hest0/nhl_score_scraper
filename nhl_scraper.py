import csv
import datetime
import requests
from bs4 import BeautifulSoup

#first the url to scrape
url = 'https://www.quanthockey.com/nhl/nationality/finnish-nhl-players-2022-23-stats.html'

#send a request to the URL to get the HTML content
response = requests.get(url)
html = response.content

#create an object to parse HTML
soup = BeautifulSoup(html, 'html.parser')

#get the date of the stats from the page title
now = datetime.datetime.now()
date_str = now.strftime("%Y-%m-%d")
filename = f"nhl_stats_{date_str}.csv"

#search for players with points last night
rows = soup.select('tr.fin td:nth-of-type(10):not(:-soup-contains("0"))')

#create a list to store the stats
stats = []