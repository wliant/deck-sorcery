from DataProvider import *
from sklearn import svm

heroClasses = ["DRUID", "HUNTER", "MAGE", "PALADIN", "PRIEST", "ROGUE", "SHAMAN", "WARLOCK", "WARRIOR"]

predictor = {}

cs = getCardStats()
deckStats = getDeckStats()

cardStats = {}
for cl in cs:
    for crd in cs[cl]:
        if crd["dbf_id"] not in cardStats:
            cardStats[crd["dbf_id"]] = {}
        cardStats[crd["dbf_id"]][cl] = {"popularity": crd["popularity"], "winrate": crd["winrate"], "total":crd["total"]}

print(len(cardStats.keys()))

def calculateUniqueCount(cardArray):
    cards = set()
    for c in cardArray:
        cards.add(c)
    return len(cards)

def calculateTypeCount(cardType, cardArray):
    cards = [c for c in cardArray if getCardType(c) == cardType]
    return len(cards)

def calculateClassCardCount(cardArray):
    cards = [c for c in cardArray if getCardClass(c) != "NEUTRAL"]
    return len(cards)

def calculateAverageCardWinRate(heroClass,cardArray):
    winrates = []
    for card in cardArray:
        if card in cardStats:
            wr = cardStats[card][heroClass]["winrate"] if heroClass in cardStats[card] else cardStats[card]["ALL"]["winrate"]
            winrates.append(float(wr) if wr else 0.0)
        else:
            winrates.append(0.0)

    return sum(winrates)/len(winrates)
            

def calcualteMinionStatsRatio(cardArray):
    stats = sum([getCardHealth(c) + getCardAttack(c) for c in cardArray if getCardType(c) == "MINION"])
    cost = sum([getCardCost(c) for c in cardArray if getCardType(c) == "MINION"])
    if cost == 0:
        cost = 1
    
    return stats / cost
    
def calculateCostCount(cost, cardArray):
    if cost == 1:
        cards = [c for c in cardArray if getCardCost(c) <= 1]
    elif cost == 7:
        cards = [c for c in cardArray if getCardCost(c) >= 7]
    else:
        cards = [c for c in cardArray if getCardCost(c) == cost]
    return len(cards)

#this function convert the deck to feature array 
def convertToFeaturesArray(heroClass, deck): 

    return [calculateUniqueCount(deck),
            calcualteMinionStatsRatio(deck),
            calculateTypeCount("SPELL", deck),
            calculateTypeCount("MINION", deck),
            calculateTypeCount("HERO", deck),
            calculateTypeCount("WEAPON", deck),
            #calculateClassCardCount(deck),
            calculateCostCount(1, deck),
            calculateCostCount(2, deck),
            calculateCostCount(3, deck),
            calculateCostCount(4, deck),
            calculateCostCount(5, deck),
            calculateCostCount(6, deck),
            calculateCostCount(7, deck),
            calculateAverageCardWinRate(heroClass, deck)
        ]
        
for hc in heroClasses:
    deckFeatures = []
    winRates = []
    for deck in deckStats[hc]:
        cardArrays = [[cardId] * count for cardId, count in json.loads(deck["deck_list"])]
        cardArrays = [item for sublist in cardArrays for item in sublist]
        deckFeatures.append(convertToFeaturesArray(hc, cardArrays))
        winRates.append(deck["win_rate"])
    
    clf = svm.SVR()
    clf.fit(deckFeatures, winRates)

    predictor[hc] = clf
#deck is a list of dfid. this function return the predicted winrate of the deck
def predict(heroClass, deck):
    values = predictor[heroClass].predict([convertToFeaturesArray(heroClass, deck)])
    return values[0]