import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#ubwr

url = input("url: ")
#url = 'https://progressionfootball.com/game?league=5598&game=4101510'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

divs = soup.find_all('div', class_="play")

data = []
team_name = input("team name: ")
#team_name = 'berserkers'
week_num = input("week num: ")
#week_num = '1'

## EVERYTHING BELOW EXCLUDES PLAYS WITH TURNOVERS
## WIP

for div in divs:
    last_span = div.select('span', style_="min-width:270px;")[0]
    down = last_span.span.find_all('span')
    if len(down) >= 3:
        down = int(down[1].text[1])
        if not last_span.span.text[1].isalpha():
            quarter = int(last_span.span.text[1])
        else:
            quarter = str(last_span.span.text[1])
    if "pass" in last_span.text.lower() and "intercept" not in last_span.text.lower():
        first_image = div.find('img')['src']
        if team_name in first_image:
            match = re.search(r'(?<=pass to )\d+|\d+(?= yards)', str(last_span))
            if match:
                if "behind" in last_span.text.lower():
                    yards = '-' + (match.group(0))
                    data.append(('P', int(yards), down, quarter))
                else:
                    yards = match.group(0)
                    data.append(('P', int(yards), down, quarter))
                print(f"pass {yards} {down} {quarter}")
            else:
                yards = 0
                data.append(('P', yards, down, quarter))
                print(f"pass 0 {down} {quarter}")

    elif "ran " in last_span.text.lower() and "fumble" not in last_span.text.lower():
        first_image = div.find('img')['src']
        if team_name in first_image:
            match = re.search(r'(?<=ran )\d+|\d+(?= yards)', str(last_span))
            if match:
                if "behind" in last_span.text.lower():
                    yards = '-' + (match.group(0))
                    data.append(('R', int(yards), down, quarter))
                else:
                    yards = match.group(0)
                    data.append(('R', int(yards), down, quarter))
                print(f"run {yards} {down} {quarter}")
            else:
                yards = 0
                data.append(('R', yards, down, quarter))
                print(f"run 0 {down} {quarter}")
    elif "sacked" in last_span.text.lower():
        first_image = div.find('img')['src']
        if team_name in first_image:
            match = re.search(r'(?<=sacked )\d+|\d+(?= yards)', str(last_span))
            if match:
                yards = '-' + match.group(0)
                data.append(('P', int(yards), down, quarter))
                print(f"pass {yards} {down} {quarter}")
            else:
                yards = 0
                data.append(('P', yards, down, quarter))
                print(f"pass 0 {down} {quarter}")


keys, values, labels, quarters_ = zip(*data)

x_values = range(len(keys))

rush_indices = [i for i, key in enumerate(keys) if key == "R"]
nonrush_indices = [i for i in x_values if i not in rush_indices]

plt.bar(nonrush_indices, [values[i] for i in nonrush_indices], align='center', color='dodgerblue')
plt.bar(rush_indices, [values[i] for i in rush_indices], align='center', color='red')

plt.xticks(x_values, keys)

for i in rush_indices:
    plt.gca().get_xticklabels()[i].set_color('red')

for i in nonrush_indices:
    plt.gca().get_xticklabels()[i].set_color('dodgerblue')

for i in range(len(labels)):
    plt.text(x_values[i], values[i], labels[i], ha='center', va='bottom')

plt.grid(alpha=0.2)

plt.xlabel('Play Type')
plt.ylabel('Yardage')
plt.title(team_name+' Yardage Per Play Week ' + week_num)
plt.savefig(team_name+' Yardage Per Play Week ' + week_num + '.png')
#plt.show()
plt.clf()

#####################################################################################################

quarters = {}
for play in data:
    quarter = play[3]
    if quarter not in quarters:
        quarters[quarter] = {}
    play_type = play[0]
    if play_type not in quarters[quarter]:
        quarters[quarter][play_type] = 0
    quarters[quarter][play_type] += 1

for quarter, plays in quarters.items():
    total_plays = sum(plays.values())
    for play_type in plays:
        plays[play_type] = plays[play_type] / total_plays * 100

for key, value in quarters.items():
    qlabels = list(value.keys())
    qvalues = list(value.values())

    colors = []

    for color_key in value.keys():
        if color_key == 'R':
            colors.append('red')
        else:
            colors.append('dodgerblue')

    plt.pie(qvalues, labels=qlabels, autopct='%1.1f%%', colors=colors)

    plt.title(f'{team_name} play data for Quarter {key} Week {week_num}')

    plt.savefig(f'{team_name} play data for Quarter {key} Week {week_num}'+'.png')
    #plt.show()
    plt.clf()

#####################################################################################################

downs = {}
for play in data:
    down = play[2]
    if down not in downs:
        downs[down] = {}
    play_type = play[0]
    if play_type not in downs[down]:
        downs[down][play_type] = 0
    downs[down][play_type] += 1

for down, plays in downs.items():
    total_plays = sum(plays.values())
    for play_type in plays:
        plays[play_type] = plays[play_type] / total_plays * 100

for key, value in downs.items():
    dlabels = list(value.keys())
    dvalues = list(value.values())

    colors = []

    for color_key in value.keys():
        if color_key == 'R':
            colors.append('red')
        else:
            colors.append('dodgerblue')

    plt.pie(dvalues, labels=dlabels, autopct='%1.1f%%', colors=colors)

    plt.title(f'{team_name} play data for down {key} Week {week_num}')

    plt.savefig(f'{team_name} play data for down {key} Week {week_num}'+'.png')
    #plt.show()
    plt.clf()