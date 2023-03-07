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

#loop through players with points
for row in rows:
    
    name = row.select_one('td.player-name > a').text

    #get goals and assists
    goals = row.select_one('td:nth-of-type(5)').text
    assists = row.select_one('td:nth-of-type(6)').text

    #add the stats to the list 'stats'
    stats.append([date_str, name, goals, assists])

#save stats to CSV file
with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'name', 'goals', 'assists'])
    writer.writerows(stats)

#open the CSV file
import subprocess
subprocess.call(['open', '-a', 'Numbers', filename])