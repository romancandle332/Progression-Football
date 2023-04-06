from urllib.request import urlopen
from bs4 import BeautifulSoup
from PFLibrary import *
import re
import csv
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
                continue
            elif "Kickoff" in pl:
                continue
            elif "FG" in pl:
                continue
            if "midfield" in pl:
                i = pl.index("midfield")
                pl[i] = 50
                pl.insert(i,pl[0])
            subset.append(pl)
    teamone = ""
    teamtwo = ""
    for sub in subset:
        if teamone == "":
            teamone = sub[0]
        elif sub[0] != teamone:
            teamtwo = sub[0]
            break
    for sub in subset:
        possession = sub[0]
        if sub[0] == teamone:
            defense = teamtwo
        elif sub[0] == teamtwo:
            defense = teamone
        quarter = sub[1]
        down = sub[3]
        distance = sub[5]
        spot = sub[7]
        blitz = False
        turnover = False
        sack = False
        if "Touchdown!" in sub:
            if "intercepted" in sub or "Recovered" in sub:
                score = -7
            else:
                score = 7
        elif "FG attempt" in sub and "is good!" in sub:
            score = 3
        else:
            score = 0
        if possession == spot:
            goal = 100 - int(sub[8])
        else:
            goal = int(sub[8])
        if "ran" in sub:
            playtype = "Run"
            if "no" in sub:
                yards = 0
            elif "fumbled!" in sub:
                y = sub.index("of")
                turnover = True
                yards = sub[y+1]
            else:
                y = sub.index("for")
                yards = sub[y+1]
        elif "scrambled" in sub:
            playtype = "Run"
            if "no" in sub:
                yards = 0
            elif "fumbled!" in sub:
                y = sub.index("of")
                turnover = True
                yards = sub[y+1]
            else:
                y = sub.index("for")
                yards = sub[y+1]
        elif "sacked" in sub:
            playtype = "Pass"
            sack = True
            y = sub.index("for")
            yards = sub[y+1]
        elif "pass" in sub:
            playtype = "Pass"
            if "intended" in sub:
                if "intercepted" in sub:
                    y = sub.index("of")
                    turnover = True
                    yards = -1*int(sub[y+1])
                else:
                    yards = 0
            else:
                y = sub.index("for")
                yards = sub[y+1]
        if "BLITZ!" in sub:
            blitz = True
        boxscore.append([possession,defense,quarter,down,distance,goal,playtype,yards,blitz,turnover,sack,score])

    filename = "EloByPlay/"+str(game)+".csv"
    with open(filename, "w") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerows(boxscore)
