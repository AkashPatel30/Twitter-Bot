import requests
from bs4 import BeautifulSoup
import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

#Get HTML page
URL = 'https://www.basketball-reference.com/wnba/players/c/clarkca02w.html'
page = requests.get(URL)

#Autheticate Twitter
auth = tweepy.OAuthHandler(os.getenv('api_key'),os.getenv('api_secret_key') )
auth.set_access_token(os.getenv('token'),os.getenv('secret_token'))

api = tweepy.API(auth)

"Parse through HTML"
soup = BeautifulSoup(page.content, 'html.parser')

#Find HTML element by id
results = soup.find(id='div_last5')
table_body = results.find('tbody')
rows = table_body.find_all('tr')

#Extract from latest game
latest = rows[0]

#Extract elemts with attribute 'data-stat'
stat_elements = latest.find_all(attrs={'data-stat':True })

stats = {}

# Extract the data
for elem in stat_elements:
    stat_name = elem['data-stat']
    stat_value = elem.text.strip()
    stats[stat_name] = stat_value

#Turn elements in the dictionary to int
steals = int(stats['stl'])
blocks = int(stats['blk'])

#Create tweet to be posted
tweet = f"Caitlin Clark tonight: \n\n{stats['pts']} PTS \n{stats['trb']} REB \n{stats['ast']} AST"

#Check if steals/blocks are worth posting
if steals>0:
    tweet += f"\n{steals} STL"

if blocks>0:
    tweet += f"\n{blocks} BLK"

#Show what the tweet will look like
print(tweet)

#Post tweet if Elon Musk didnt ruin the app
api.update_status(tweet)    