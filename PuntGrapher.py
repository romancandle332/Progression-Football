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
class Punter():
    def __init__(self,name):
        self.name = name
        self.punts = []

    def AddPunt(self,yards,score):
        self.punts.append([yards,score])

punters = []       
for game in games:
    boxscore = []
    filename = "Punts/"+str(game)+".csv"
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            boxscore.append(row)
    for snap in boxscore:
        name = snap[2]
        yards = int(snap[3])
        scrimmage = int(snap[4])
        possible = int(snap[5])
        distance = int(snap[6])
        if yards >= possible:
            score = (possible - 20)/possible
        else:
            score = yards/possible
        found = False
        for punter in punters:
            if punter.name == name:
                found = True
                punter.AddPunt(yards,score)
        if found == False:
            x = Punter(name)
            x.AddPunt(yards,score)
            punters.append(x)

buckx = []
bucky = []
bucklabel = []
for punter in punters:
    total = 0
    yards = 0
    score = 0
    for punt in punter.punts:
        total += 1
        yards += punt[0]
        score += punt[1]
    yardavg = round(yards / total,2)
    grade = round(score / total,2)
    name = punter.name
    print(name,yardavg,grade)
    buckx.append(yardavg)
    bucky.append(grade)
    bucklabel.append(name)
xavg = np.average(buckx)
yavg = np.average(bucky)
fig, ax = plt.subplots()
ax.scatter(buckx,bucky)
for x,y,z in zip(buckx,bucky,bucklabel):
    plt.annotate(z,(x,y),textcoords="offset points",xytext=(0,5), fontsize = 10)
plt.title("Punting Average")
plt.xlabel("Avg Punt Distance (pre-return)")
plt.ylabel("100 - Opp Starting Position")
plt.axvline(x=xavg,color='red',ls=':',label = 'Off Avg')
plt.axhline(y=yavg,color='blue',ls=':',label = 'Def Avg')
plt.rcParams["figure.figsize"] = (50,50)
plt.savefig('PuntingPlot.png')
plt.show()
