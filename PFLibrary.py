##Official League ID
league = str(5598)

##Running list of game ###s, +1 because that's just what do
games = range(4101506,4101586)

##Current week of games so you don't scrape the whole season every time
currentweek = range(4101586,4101602)


PFAbb = {"Roadrunners": "ARI",
        "Hawks": "ATL",
        "Owls": "BAL",
        "Bulls": "BUF",
        "Raptors": "CAR",
        "Berserkers": "CHI",
        "Bluecats": "CIN",
        "Bulldogs": "CLE",
        "Sheriffs": "DAL",
        "Stallions": "DEN",
        "Prowlers": "DET",
        "Wolverines": "GB",
        "Coyotes": "HOU",
        "Dragons": "IND",
        "Wildcats": "JAX",
        "Natives": "KC",
        "Vigilantes": "LV",
        "Griffins": "LAG",
        "Rhinos": "LAR",
        "Sharks": "MIA",
        "Polar bears": "MIN",
        "Marauders": "NE",
        "Boars": "NO",
        "Hornets": "NYH",
        "Paladins": "NYP",
        "Tyrants": "PHI",
        "Demons": "PIT",
        "Miners": "SF",
        "Kings": "SEA",
        "Pirates": "TB",
        "Vipers": "TEN",
        "Bandits": "WAS"}

##Team Object for ultimate flexibility as I add more functionality
class Team:
    def __init__(self,city,nickname,abbreviation,conference,division):
        self.city = city
        self.nickname = nickname
        self.abbr = abbreviation
        self.conference = conference
        self.division = division
        self.EloOff = 1500
        self.EloDef = 1500
        self.OffSnaps = 0
        self.OffWins = 0
        self.DefSnaps = 0
        self.DefWins = 0
        self.Games = []
    def GetImage(self):
        lowercase = self.nickname.lower()
        filename = "icons/"+lowercase+".svg"
        return filename
    def AddGame(self,opponent,pf,pa):
        self.Games.append([opponent,pf,pa])

##I wanna turn this into a CSV load function somehow for easier editing
ARI = Team("Arizona","Roadrunners","ARI","Blue","West")
ATL = Team("Atlanta","Hawks","ATL","Blue","South")
BAL = Team("Baltimore","Owls","BAL","Red","North")
BUF = Team("Buffalo","Bulls","BUF","Red","East")
CAR = Team("Carolina","Raptors","CAR","Blue","South")
CHI = Team("Chicago","Berserkers","CHI","Blue","North")
CIN = Team("Cincinnati","Bluecats","CIN","Red","North")
CLE = Team("Cleveland","Bulldogs","CLE","Red","North")
DAL = Team("Dallas","Sheriffs","DAL","Blue","East")
DEN = Team("Denver","Stallions","DEN","Red","West")
DET = Team("Detroit","Prowlers","DET","Blue","North")
GB = Team("Green Bay","Wolverines","GB","Blue","North")
HOU = Team("Houston","Coyotes","HOU","Red","South")
IND = Team("Indianapolis","Dragons","IND","Red","South")
JAX = Team("Jacksonville","Wildcats","JAX","Red","South")
KC = Team("Kansas City","Natives","KC","Red","West")
LV = Team("Las Vegas","Vigilantes","LV","Red","West")
LAG = Team("Los Angeles","Griffins","LAG","Red","West")
LAR = Team("Los Angeles","Rhinos","LAR","Blue","West")
MIA = Team("Miami","Sharks","MIA","Red","East")
MIN = Team("Minnesota","Polar Bears","MIN","Blue","North")
NE = Team("New England","Marauders","NE","Red","East")
NO = Team("New Orleans","Boars","NO","Blue","South")
NYH = Team("New York","Hornets","NYH","Red","East")
NYP = Team("New York","Paladins","NYP","Blue","East")
PHI = Team("Philadelphia","Tyrants","PHI","Blue","East")
PIT = Team("Pittsburgh","Demons","PIT","Red","North")
SF = Team("San Francisco","Miners","SF","Blue","West")
SEA = Team("Seattle","Kings","SEA","Blue","West")
TB = Team("Tampa Bay","Pirates","TB","Blue","South")
TEN = Team("Tennessee","Vipers","TEN","Red","South")
WAS = Team("Washington","Bandits","WAS","Blue","East")

##List ALL the teams!
PFTeams = [ARI,ATL,BAL,BUF,CAR,CHI,CIN,CLE,DAL,DEN,DET,GB,HOU,IND,JAX,KC,LV,LAG,LAR,MIA,MIN,NE,NO,NYH,NYP,PHI,PIT,SF,SEA,TB,TEN,WAS]


def AbbToTeam(x):
    return eval(x)

def ImageConvert(image):
    y = image.replace(".svg","")
    z = y.replace("/images/","")
    d = z.capitalize()
    out = PFAbb[d]
    return out
