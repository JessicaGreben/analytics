from requests import get, post
from base64 import b64encode
from csv import DictWriter
from time import strftime
from dateutil import parser
import os


client_key = os.environ['TWITTER_KEY']
client_secret = os.environ['TWITTER_SECRET']
basic_token = b64encode(':'.join([client_key, client_secret]).encode()).decode('utf-8')

bearer = post(
    'https://api.twitter.com/oauth2/token',
    headers={
        'Authorization': 'Basic ' + basic_token,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    },
    data={
        'grant_type': 'client_credentials'
    },
)
bearer_token = bearer.json()['access_token']

tweets = get(
    'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=EconTalker',
    headers={
        'Authorization': 'Bearer ' + bearer_token,
    },
)
with open('tweets.csv', 'w') as csvfile:
    fieldnames = ['created_at', 'retweet_count', 'favorite_count', 'text']
    writer = DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for tweet in tweets.json():
        writer.writerow({
            'created_at': parser.parse(tweet['created_at']).strftime("%Y%m%d %H:%M:%S"),
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count'],
            'text': tweet['text'],
        })
