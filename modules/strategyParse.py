import csv

actions = {
    1: "hit",
    2: "stand",
    3: "split",
    4: "double or hit",
    5: "double or stand"
}

strategyFile = "files/blackjackstrategychart.csv"
strategyFile = open(strategyFile, "r")
strategyReader = csv.reader(strategyFile, delimiter=",")

def parseStrategy():
    for row in strategyReader:
        print(row)
        break
