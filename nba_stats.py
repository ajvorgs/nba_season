import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

data = requests.get('http://tv5.espn.com/nba/table')
soup = BeautifulSoup(data.text, 'html.parser')

# get Table title
Table_title = [a.text for a in soup.find_all('div', {'class', 'Table2__Title'})]
Rank = [b.text for b in soup.find_all('span', {'class', 'team-position'})]
Team = [c.text for c in soup.find_all('span', {'class', 'hide-mobile'})]
Stat = [d.text for d in soup.find_all('span', {'class', 'stat-cell'})]
Clinch = [e.text for e in soup.find_all('span', {'class', 'dib pl1'})]

def chunks(data, count):
    for i in range(0, len(data), count):
        yield data[i:i+count]

stats = list(chunks(Stat, 13))
row_data = [Table_title, Rank, Team, stats]

nbadate = date.today().strftime("%d%m%Y")
filename = 'NBA_STATS_as_at_' + nbadate + '.csv'


with open(filename,'w') as f:
        csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, lineterminator='\n')
        csv_writer = csv.writer(f,dialect='myDialect')
        csv_writer.writerow(['Region','Team', 'W','L','PCT','GB','Home','Away','DIV','Conf','PPG','OPP PPG','DIFF','STRK','L10'])
        
        for x in range(15):
                csv_writer.writerow([row_data[0][0], row_data[2][x], *row_data[3][x]])

        for x in range(15,30):
                csv_writer.writerow([row_data[0][1], row_data[2][x], *row_data[3][x]])