#this file handle all the reading and writing of data files

import csv
import json
#cards will hold a list of class dictonary object 

cardJsonFile = "data/cards-in-use.json"
cardCsvFile = "data/cards-wild.csv"

cards = []
cards2 = []
#data processing cards data
with open(cardJsonFile, "rb") as infile:
    #load from json file
    cards = json.load(infile)

with open(cardCsvFile,encoding ="ISO-8859-1") as infile:
    reader = csv.reader(infile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    cards2 = [r for r in reader]

# validate card names from csv file match with json file
for card in cards2:
    result = [a for a in cards if a["name"] == card[0] and ("set" not in a or a["set"] != "HERO_SKINS")]
    if len(result) != 1:
        print("{0}: found {1}".format(card[0], len(result)))

myCardList = []
for card in cards2:
    searchResult = [a for a in cards if a["name"] == card[0] and ("set" not in a or a["set"] != "HERO_SKINS")]
    matchedCard = searchResult[0]

    cardId = matchedCard["dbfId"]
    name = card[0]
    cardType = matchedCard["type"]
    cardRarity = matchedCard["rarity"]
    cardClass = matchedCard["cardClass"]
    cardRace = matchedCard["race"] if "race" in matchedCard else ""
    health = card[6]
    attack = card[7]
    cost = card[5]
    durability = card[8]
    myCardList.append({
        "id": cardId,
        "name": name,
        "type": cardType,
        "rarity": cardRarity,
        "class": cardClass,
        "race": cardRace,
        "health": health,
        "attack": attack,
        "cost": cost,
        "durability": durability
    })

cardDict = {c["id"]: c for c in myCardList}

def getAllCards():
    return myCardList

def getAvailableCardIdsForConstruction(heroClass): 
    return [c["id"] for c in myCardList if c["class"].lower() in [heroClass.lower(), "neutral"]]

def getRarity(cardId):
    return cardDict[cardId]["rarity"]

def getCardName(cardId):
    return cardDict[cardId]["name"]

def getAllHeroClass():
    classes = [card['class'] for card in myCardList]
    return list(dict.fromkeys(classes))

def getCardsForHero(heroClass):
    cardsForHero=[card for card in myCardList if card['class'] == heroClass]
    print(cardsForHero)
    return cardsForHero
