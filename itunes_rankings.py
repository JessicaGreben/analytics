from requests import get
from csv import DictWriter
from itunes_country_code import country_codes
import os
import datetime

# collectionIDs are all the IDs of the different EconTalk podcasts on iTunes Store, which includes all the archived years.
collectionIDs = [135066958, 279314489, 279314447, 305422538, 360959737, 596439841, 596443450, 972057805, 787114107, 971760319, 455989998, 420545936]

# genreNameIds are a mapping of the genres names to their ID
# These genres are related to EconTalk for iTunes podcasts
# ref: https://affiliate.itunes.apple.com/resources/documentation/genre-mapping/
genreIdsNames = {
	1416: "Higher Education",
	26: "Podcasts",
	1304: "Education",
	1315: "Science & Medicine",
	1479: "Social Sciences",
	1321: "Business",
}

def writeCSVheader():
	with open('itunes_rankings.csv', 'a') as csvfile:
	    fieldnames = ['title', 'date', 'country', 'genre', 'ranking']
	    writer = DictWriter(csvfile, fieldnames=fieldnames)
	    writer.writeheader()

def getAndSaveData(url, country, genre):
	reviews = get(url)

	now = datetime.datetime.now()
	with open('itunes_rankings.csv', 'a') as csvfile:

	    try:
	    	reviews.json()["feed"]["entry"]
	    except:
	    	return

	    ranking = 0
	    for review in reviews.json()["feed"]["entry"]:
	    	ranking += 1

	    	try:
	    		review["im:name"]["label"]
	    	except:
	    		continue

	    	if "EconTalk" in review["im:name"]["label"]:
				with open('itunes_rankings.csv', 'a') as csvfile:
					fieldnames = ['title', 'date', 'country','genre','ranking']
					writer = DictWriter(csvfile, fieldnames=fieldnames)
				  	writer.writerow({
				    	'title': review["im:name"]["label"].encode('utf8'),
				    	'date': now.strftime("%Y-%m-%d"),
				    	'country': country,
				    	'genre': genre,
				    	'ranking': ranking,
				    })

writeCSVheader()

for abbr in country_codes:
	print "abbr:", abbr
	for genre in genreIdsNames:
		print "genre:", genre
		rankingsURL = "https://itunes.apple.com/{}/rss/toppodcasts/genre={}/limit=200/json".format(abbr, genre)
		getAndSaveData(rankingsURL, country_codes[abbr], genreIdsNames[genre])
