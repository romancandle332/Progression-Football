from urllib.request import urlopen
from bs4 import BeautifulSoup
from PFLibrary import *
import re
import csv
league = str(5598)
games = range(4101554,4101586)
for subgame in games:
    game = str(subgame)
    url = "https://progressionfootball.com/game?league="+league+"&game="+game
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    plays = soup.find('div', id = "plays")
    boxscore = []
    subset = []
    for play in plays:
        if play == "\n":
            pass
        else:
            image = play.find("img")
            convert = str(image['src'])
            possession = ImageConvert(convert)
            y = possession +" " + ' '.join(play.stripped_strings)
            pl = y.split(" ")
            if "Punt" in pl:
                if "midfield" in pl:
                    i = pl.index("midfield")
                    pl[i] = 50
                    pl.insert(i,pl[0])
                subset.append(pl)
            else:
                continue
    teamone = ""
    teamtwo = ""
    for sub in subset:
        if teamone == "":
            teamone = sub[0]
        elif sub[0] != teamone:
            teamtwo = sub[0]
            break
    for sub in subset:
        if "midfield)." in sub:
            w = sub.index("midfield).")
            sub[w] = "50"
        possession = sub[0]
        if sub[0] == teamone:
            defense = teamtwo
        elif sub[0] == teamtwo:
            defense = teamone
        quarter = sub[1]
        punter_first = sub[12]
        punter_last = sub[13]
        punter_name = punter_first+ " "+punter_last
        distance = sub[5]
        spot = sub[8]
        if sub[7] == sub[0]:
            goal = 100 - int(sub[8])
        else:
            goal = int(sub[8])
        y = sub.index("for")
        yards = int(sub[y+1])
        if "Touchback." in sub:
            result = 20
        else:
            if sub[-2] == sub[0]:
                result = 100 - int(re.sub("[^0-9]", "",sub[-1]))
            else:
                result = int(re.sub("[^0-9]", "",sub[-1]))
        net = 100 - result
        boxscore.append([possession,defense,punter_name,yards,spot,goal,result,net])
    filename = "Punts/"+str(game)+".csv"
    with open(filename, "w") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerows(boxscore)
