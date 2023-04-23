import csv
import datetime
import requests
from bs4 import BeautifulSoup

url = 'https://www.quanthockey.com/nhl/nationality/finnish-nhl-players-2022-23-stats.html'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

now = datetime.datetime.now()
date_str = now.strftime("%Y-%m-%d")
filename = f"nhl_stats_{date_str}.csv"

rows = soup.select('tr.fin td:nth-of-type(10):not(:-soup-contains("0"))')

stats = []

for row in rows:
    
    name = row.select_one('td.player-name > a').text

    goals = row.select_one('td:nth-of-type(5)').text
    assists = row.select_one('td:nth-of-type(6)').text

    stats.append([date_str, name, goals, assists])

with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'name', 'goals', 'assists'])
    writer.writerows(stats)

import subprocess
subprocess.call(['open', '-a', 'Numbers', filename])