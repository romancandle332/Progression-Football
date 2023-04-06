import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from svgpathtools import svg2paths
from svgpath2mpl import parse_path
from PFLibrary import *
boxscore = []
with open("gametable.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        boxscore.append(row)
for snap in boxscore:
    team1 = AbbToTeam(snap[0])
    score1 = int(snap[1])
    score2 = int(snap[2])
    team2 = AbbToTeam(snap[3])
    team1.AddGame(team2.abbr,score1,score2)
    team2.AddGame(team1.abbr,score2,score1)

teams = []
offense = []
defense = []
for team in PFTeams:
    games = team.Games
    pftotal = 0
    patotal = 0
    gamesplayed = 0
    for game in games:
        opponent = AbbToTeam(game[0])
        pf = game[1]
        pa = game[2]
        opf = 0
        opa = 0
        opg = 0
        for subgame in opponent.Games:
            if subgame[0] != team.abbr:
                opf += subgame[1]
                opa += subgame[2]
                opg += 1
        pfp = pf - opa/opg
        pap = pa - opf/opg
        pftotal += pfp
        patotal += pap
        gamesplayed += 1
    teams.append(team.abbr)
    offense.append(pftotal / gamesplayed)
    defense.append(patotal / gamesplayed)
offavg = np.average(offense)
defavg = np.average(defense)
fig, ax = plt.subplots()
ax.scatter(offense,defense)
for x,y,z in zip(offense,defense,teams):
    plt.annotate(z,(x,y),textcoords="offset points",xytext=(0,5))
plt.title("PF/G, PA/G adjusted for Opponents")
plt.xlabel("Points For / Game")
plt.ylabel("Points Against / Game")
plt.axvline(x=offavg,color='red',ls=':',label = 'Off Avg')
plt.axhline(y=defavg,color='blue',ls=':',label = 'Def Avg')
ax.invert_yaxis()
plt.savefig('PFPAPlus.png')
plt.show()
