from requests import get, post
from base64 import b64encode
from csv import DictWriter
from time import strftime
from dateutil import parser
from json import dumps
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

# https://api.twitter.com/1.1/tweets/search/fullarchive/econtalks.json" -d ''
search_url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/econtalks.json'
with open('tweets.csv', 'w') as csvfile:
    fieldnames = ['created_at', 'retweet_count', 'favorite_count', 'text']
    writer = DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    next_param = None
    while True:
        params = {'query': 'from:EconTalker', 'fromDate': '201512220000'}
        if next_param:
            params['next'] = next_param

        tweets = post(
            search_url,
            headers={
                'Authorization': 'Bearer ' + bearer_token,
            },
            data=dumps(params),
        )
        tweets_json = tweets.json()

        if tweets.status_code != 200:
            print(tweets_json)
            break

        for tweet in tweets_json['results']:
            writer.writerow({
                'created_at': parser.parse(tweet['created_at']).strftime("%Y%m%d %H:%M:%S"),
                'retweet_count': tweet['retweet_count'],
                'favorite_count': tweet['favorite_count'],
                'text': tweet['text'],
            })

        if 'next' in tweets_json:
            next_param = tweets_json['next']
        else:
            break
