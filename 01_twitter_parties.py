#  Collecting tweets from Bosnian actors in real time.


# (c) Annerose Nisser, 2016-07-27

# THIS SCRIPT SHOULD RUN ON PYTHON 2!
# ****************************** #
# https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
# https://apps.twitter.com/app/7745525/keys
# https://dev.twitter.com/rest/reference/get/users/show
#  http://docs.tweepy.org/en/v3.5.0/
# https://dev.twitter.com/streaming/overview/request-parameters
# http://stats.seandolinar.com/collecting-twitter-data-using-a-python-stream-listener/

from tweepy import OAuthHandler
from tweepy import API
import json
import time
import os
from sys import platform
import config # local config file to store password and user keys etc.

print "Started running script twitter_parties.py at %s" % time.ctime()

try:
	ckey = config.ckey
	consumer_secret = config.consumer_secret
	access_token_key = config.access_token_key
	access_token_secret = config.access_token_secret
except:
	print """	Please specify your Twitter key, access token etc.
	See
	https://dev.twitter.com/oauth/overview/application-owner-access-tokens
	for more info"""


tweeters = ['HRHercegBosna', 'sdpbih', 'sbb_bih', 'bihhdz', 'radomzaboljitak',
			'snsddodik', 'sdsrscom', 'pdp_rsrpska', 'srpskars', 'HercegBosna',
			'HSPHercegBosne', 'VladaRH', 'HRHBInfo', 'MiloradDodikRS',
			'predsjednikrs' ,
			'VladaRBiH', 'klixba']

# ids of those tweeters (not necessary for this script)
# tweeters = ['448388602', '189098732', '148671858', '738759373623808000',
# 			'144830871', '186938977', '348406632', '4121142125',
# 			'1388068356', '99956790', '452379248', '444097675',
# 			'309046075', '1097720455', '1097720124', '2928919282', '48104665']


auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)

# ****************************************** #
# http://stackoverflow.com/questions/15628535/how-can-i-retrieve-all-tweets-and-attributes-for-a-given-user-using-python?rq=1
# https://github.com/tweepy/tweepy/issues/519
api = API(auth)

# user = api.get_user("klixba")
counter = 0

tweet_ids = []

# Define the place of the document depending on whether the script
# runs on the local machine or on the server (server is linux-based):
if platform == "darwin":
	doc_path = 'data/tweets/bosnian_politicians_tweets.txt'
if platform == "linux" or platform == "linux2":
	doc_path = '/home/annerose/Python/bosnian_politicians_tweets.txt'


try: # if file is already existent
	with open(doc_path, 'r+') as f:

		# get tweet_ids from the existing file:
		objs_string = f.read()
		objs = json.loads(objs_string)
		tweet_ids = [tweet['id'] for tweet in objs]

		# Delete last "]"
		f.seek(-1, os.SEEK_END)
		f.truncate()
		f.write(u',') # add comma after last tweet from file.


except: # if file doesn't exist, create it and add "[" at the very beginning.
	print "Not opened"
	with open(doc_path, 'w+') as f:
		f.write(u'[')



# define on how to add tweets of a given user to the txt file:
def getusertweets(user, tweet_ids = tweet_ids):
	global counter
	timeline = api.user_timeline(screen_name = user, # user_id=tweeters,
					  include_rts=True,
					  exclude_replies = False,
					  count=200)

	for tweet in timeline:
		tweet = json.dumps(tweet._json) # http://stackoverflow.com/questions/27900451/convert-tweepy-status-object-into-json
		tweet = json.loads(tweet)
		# print("Got tweet of user: %s" % tweet['user']['screen_name'])

		# check whether tweet already exist in json data:
		if tweet['id'] not in tweet_ids:
			with open(doc_path, 'a+') as outfile:
				json.dump(tweet, outfile)
				outfile.write(u',\n') # add comma and newline
				print "Wrote new tweet to file (user %s)" % tweet['user']['screen_name']
				counter += 1



# Write text as normal for every user/tweeter:
for tweeter in tweeters:
	getusertweets(tweeter)

# As script finishes, make changes in the last
# characters of the txt document:
if counter>0:
	last = -2
if counter==0: # if no new tweets were added.
	last = -1
with open(doc_path, 'a+') as f:
	# Delete last "\n" and last ","
	f.seek(last, os.SEEK_END)
	f.truncate()

	# Add last "]"
	f.write(u']')
	# Close file.


# Tell how many new tweets were added to the file.
print "Finished running script twitter_parties.py at %s" % time.ctime()
print "Wrote %d new tweets to file" % counter
