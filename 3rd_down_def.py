import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#ubwr

base_url = 'https://progressionfootball.com'

start_week = 1
num_weeks = 4
schedule_url = 'https://progressionfootball.com/schedule?league=5598&season=1&week=' + str(num_weeks)
response = requests.get(schedule_url)
soup = BeautifulSoup(response.content, 'html.parser')

games_divs = soup.find_all('div', class_="row")

all_games_list = []

team_list = ['roadrunners', 'hawks', 'owls', 'bulls', 'raptors', 'berserkers', 'bluecats', 'bulldogs', 'sheriffs', 'stallions',
 'prowlers', 'wolverines', 'coyotes', 'dragons', 'wildcats', 'natives', 'vigilantes', 'griffins', 'rhinos',
 'sharks', 'polar bears', 'marauders', 'boars', 'hornets', 'paladins', 'tyrants', 'demons', 'miners',
 'kings', 'pirates', 'vipers', 'bandits']

team_dict = {
    'roadrunners': [0, 0],
    'hawks': [0, 0],
    'owls': [0, 0],
    'bulls': [0, 0],
    'raptors': [0, 0],
    'berserkers': [0, 0],
    'bluecats': [0, 0],
    'bulldogs': [0, 0],
    'sheriffs': [0, 0],
    'stallions': [0, 0],
    'prowlers': [0, 0],
    'wolverines': [0, 0],
    'coyotes': [0, 0],
    'dragons': [0, 0],
    'wildcats': [0, 0],
    'natives': [0, 0],
    'vigilantes': [0, 0],
    'griffins': [0, 0],
    'rhinos': [0, 0],
    'sharks': [0, 0],
    'polar bears': [0, 0],
    'marauders': [0, 0],
    'boars': [0, 0],
    'hornets': [0, 0],
    'paladins': [0, 0],
    'tyrants': [0, 0],
    'demons': [0, 0],
    'miners': [0, 0],
    'kings': [0, 0],
    'pirates': [0, 0],
    'vipers': [0, 0],
    'bandits': [0, 0]
}

converted = 0
not_converted = 0

for week in range(start_week, num_weeks):
    schedule_url = 'https://progressionfootball.com/schedule?league=5598&season=1&week=' + str(week)
    response = requests.get(schedule_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    games_divs = soup.find_all('div', class_="row")
    for div in games_divs:
        game = str(div.select('a', class_="href"))
        if len(game) > 2:
            soup = BeautifulSoup(game, 'html.parser')
            link = soup.find('a')['href']
            all_games_list.append(str(base_url+link))
for game in all_games_list:
    print(game)
    response = requests.get(game)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_="col-sm-4 text-center mt-2 mb-2")
    game_teams = []
    for div in divs:
        a_tags = div.find_all('a')
        if len(a_tags) > 0:
            for name in team_list:
                if name in a_tags[1].text.lower():
                    game_teams.append(name)
    divs = soup.find_all('div', class_="play")
    for div in divs:
        last_span = div.select('span', style_="min-width:270px;")[0]
        down = last_span.span.find_all('span')
        text = last_span.text.lower()
        team = str(div.find('img')['src']).split("/")[2].split(".")[0]
        if len(down) >= 3:
            down = int(down[1].text[1])
        if down == 3:
            if "first" in text:
                for name in game_teams:
                    if team != name:
                        team_dict[name][0] += 1
            else:
                if "intercept" not in text and "fumble" not in text:
                    if "touchdown" in text:
                        for name in game_teams:
                            if team != name:
                                team_dict[name][0] += 1
                    else:
                        for name in game_teams:
                            if team != name:
                                team_dict[name][1] += 1
                else:
                    for name in game_teams:
                        if team != name:
                            team_dict[name][1] += 1
    game_teams = []
for t in team_dict:
    team_dict[t][1] = team_dict[t][0]+team_dict[t][1]
print(team_dict)
