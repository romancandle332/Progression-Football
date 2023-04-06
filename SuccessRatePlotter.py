import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from svgpathtools import svg2paths
from svgpath2mpl import parse_path
from PFLibrary import *
games = range(4101506,4101585)
k = 10
counter = 0
for game in games:
    boxscore = []
    filename = "EloByPlay/"+str(game)+".csv"
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            boxscore.append(row)
    for snap in boxscore:
        offense = AbbToTeam(snap[0])
        offense.OffSnaps += 1
        defense = AbbToTeam(snap[1])
        defense.DefSnaps += 1
        if snap[4] == "Goal":
            distance = int(snap[5])
        else:
            distance = int(snap[4])
        if snap[3] == "1st":
            goal = 0.4 * distance
        elif snap[3] == "2nd":
            goal = 0.6 * distance
        elif snap[3] == "3rd":
            goal = distance
        elif snap[3] == "4th":
            goal = distance
        yards = int(snap[7])
        if yards >= goal:
            offense.OffWins += 1
        elif yards < goal:
            defense.DefWins += 1
teams = []
offense = []
defense = []
for team in PFTeams:
    teams.append(team.abbr)
    offrate = team.OffWins / team.OffSnaps
    offense.append(round(offrate,2))
    defrate = team.DefWins / team.DefSnaps
    defense.append(defrate)
offavg = np.average(offense)
defavg = np.average(defense)
fig, ax = plt.subplots()
ax.scatter(offense,defense)
for x,y,z in zip(offense,defense,teams):
    plt.annotate(z,(x,y),textcoords="offset points",xytext=(0,5))
plt.title("Overall Success Rate")
plt.xlabel("Offensive")
plt.ylabel("Defensive")
plt.axvline(x=offavg,color='red',ls=':',label = 'Off Avg')
plt.axhline(y=defavg,color='blue',ls=':',label = 'Def Avg')
plt.savefig('SuccessRatePlot.png')
plt.show()
