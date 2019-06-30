from requests import get
from csv import DictWriter
import os

# collectionIDs are all the IDs of the different EconTalk podcasts on iTunes Store, which includes all the archived years.
collectionIDs = [135066958, 279314489, 279314447, 305422538, 360959737, 596439841, 596443450, 972057805, 787114107, 971760319, 455989998, 420545936]

# currently we are only looking at the data from the US, but we probably want to add
# other places where EconTalk is popular
countries = ["us"]

# genreNameIds are a mapping of the genres names to their ID
# These genres are related to EconTalk for iTunes podcasts
# ref: https://affiliate.itunes.apple.com/resources/documentation/genre-mapping/
genreNameIds = {
	"Higher Education": 1416,
	"Podcasts": 26,
	"Education": 1304,
	"Science & Medicine": 1315,
	"Social Sciences": 1479,
	"Business": 1321,
}

reviewsURL = "https://itunes.apple.com/us/rss/customerreviews/sortBy=mostRecent/json"

def getAndSaveData(url):
	reviews = get(url)

	with open('itunes_reviews.csv', 'a') as csvfile:
	    fieldnames = ['rating', 'rating_id', 'rating_author', 'rating_title']
	    writer = DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for review in reviews.json()["feed"]["entry"]:

	      writer.writerow({
	          'rating': review["im:rating"]["label"].encode('utf8'),
	          'rating_id': review["id"]["label"].encode('utf8'),
	          'rating_author': review["author"]["name"]["label"].encode('utf8'),
	          'rating_title': review["title"]["label"].encode('utf8'),
	      })

getAndSaveData(reviewsURL)

for page in range(2,7):
	print page
	x = "https://itunes.apple.com/us/rss/customerreviews/page={}/id=135066958/sortby=mostrecent/json?urlDesc=/customerreviews/id=135066958/sortBy=mostRecent/json".format(page)
	getAndSaveData(x)
