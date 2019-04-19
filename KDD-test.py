import csv
from KDD import *
testFile = "test/top7deckApril2019.csv"
testOut = "test/top7deckApril2019-result.csv"

with open(testFile,encoding ="ISO-8859-1") as infile:
    reader = csv.reader(infile)
    testDecksPre = [r for r in reader]

with open(testOut,'w', newline='') as outfile:
    writer = csv.writer(outfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    header = ["deck", "unique card", "stats-cost ratio", "spell", "minion", "hero","weapon",
            "pirate","elemental","demon","totem","dragon","murloc","mech","beast",
            "cost1-","cost2","cost3","cost4","cost5","cost6","cost7+","ruleHigh","ruleMedium","ruleLow"]
    rows = [header]
    for d in testDecksPre:
        deck = [getCardId(n) for n in d[1:]]
        fa = convertToFeaturesArray(d[0],deck)
        value = predict(d[0],deck)
        line = [str(d[1:])] + [str(a) for a in fa] + [str(value)]
        rows.append(line)
    writer.writerows(rows)
