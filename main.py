from DataProvider import * 
from flask import Flask
from flask import render_template
from flask import json
from flask import request,redirect,url_for,session
from GA import generateDeck

import random
import sys
import ast # module to transform a string to a dictionary

app = Flask(__name__)

users = {}

@app.route("/")
def index():
	return render_template("index.html"), 200

@app.route("/single")
def single():
	return render_template("single.html"), 200

@app.route("/services")
def services():
	return render_template("services.html"), 200

@app.route("/result")
def generatedResult():
	return render_template("result.html"), 200

@app.route("/getHeroes")
def getHero():
	myHeroList = getAllHeroClass()
	return json.dumps(myHeroList), 200

@app.route("/getCardsForHero")
def cardsForHero():
	heroClass = request.args.get('heroClass')
	cardsList = getCardsForHero(heroClass)
	return json.dumps(cardsList),200

@app.route("/getTheDeckForHero")
def getTheDeckForHero():
	heroClass = request.args.get('heroClass')
	print("heroClass in result "+heroClass)
	print(generateDeck(heroClass,[]))
	#return json.dumps([8,9,10,11,12]),200
	return json.dumps(generateDeck(heroClass,[])), 200



if __name__ == "__main__":
	app.run(host = "localhost", port = 3000, debug = True)
