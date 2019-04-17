from DataProvider import *
from sklearn import svm

heroClasses = ["DRUID", "HUNTER", "MAGE", "PALADIN", "PRIEST", "ROGUE", "SHAMAN", "WARLOCK", "WARRIOR"]

predictor = {}

cardStats = getCardStats()
deckStats = getDeckStats()
    
def calculateUniqueCount(cardArray):
    cards = set()
    for c in cardArray:
        cards.add(c)
    return len(cards)

def calculateSpellCount(cardArray):
    spells = [c for c in cardArray if getCardType(c) == "SPELL"]
    return len(spells)

def calculateMinionCount(cardArray):
    minions = [c for c in cardArray if getCardType(c) == "MINION"]
    return len(minions)

def calculateHeroCount(cardArray):
    heroes = [c for c in cardArray if getCardType(c) == "HERO"]
    return len(heroes)

def calculateWeaponCount(cardArray):
    weapons = [c for c in cardArray if getCardType(c) == "WEAPON"]
    return len(weapons)


def calcualteMinionStatsRatio(cardArray):
    stats = sum([getCardHealth(c) + getCardAttack(c) for c in cardArray if getCardType(c) == "MINION"])
    cost = sum([getCardCost(c) for c in cardArray if getCardType(c) == "MINION"])
    if cost == 0:
        cost = 1
    
    return stats / cost
    
#this function convert the deck to feature array 
def convertToFeaturesArray(deck): 

    return [calculateUniqueCount(deck),
            calcualteMinionStatsRatio(deck),
            calculateSpellCount(deck),
            calculateMinionCount(deck),
            calculateHeroCount(deck),
            calculateWeaponCount(deck)
        ]
        
for hc in heroClasses:
    deckFeatures = []
    winRates = []
    for deck in deckStats[hc]:
        cardArrays = [[cardId] * count for cardId, count in json.loads(deck["deck_list"])]
        cardArrays = [item for sublist in cardArrays for item in sublist]
        deckFeatures.append(convertToFeaturesArray(cardArrays))
        winRates.append(deck["win_rate"])
    
    clf = svm.SVR()
    clf.fit(deckFeatures, winRates)

    predictor[hc] = clf
#deck is a list of dfid. this function return the predicted winrate of the deck
def predict(heroClass, deck):
    values = predictor[heroClass].predict([convertToFeaturesArray(deck)])
    return values[0]