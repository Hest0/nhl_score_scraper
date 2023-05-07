import os
import csv
import datetime
import requests
from bs4 import BeautifulSoup
import mysql.connector

user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
host = os.environ.get('MYSQL_HOST')
database = os.environ.get('MYSQL_DATABASE')

url = 'https://www.quanthockey.com/nhl/nationality/finnish-nhl-players-2022-23-playoff-stats.html'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

cnx = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    database=os.environ.get('MYSQL_DATABASE')
)

cursor = cnx.cursor()

now = datetime.datetime.now()
date_str = now.strftime("%Y-%m-%d")

rows = soup.select('tr.reg:not(.tHead)')

stats = []

for row in rows:
    
    name = row.select_one('td.player-name > a').text

    goals = int(row.select_one('td:nth-of-type(5) > a')).text
    assists = int(row.select_one('td:nth-of-type(6) > a')).text

    stats.append([date_str, name, goals, assists])

insert_query = """"
INSERT INTO fin_playoff_scores_2023 (date, name, goals, assists)
VALUES (%s, %s, %s, %s)
"""
cursor.executemany(insert_query, stats)
cnx.commit()

cursor.close()
cnx.close()

import subprocess
subprocess.call(['open', '-a', 'MySQLWorkbench', '/Users/heikki/projects/Python/nhl_scores/nhl_score_scraper/nhl_stats.sql'])