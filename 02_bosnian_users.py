#  Collecting twitter network from Bosnian bloggers.


# (c) Annerose Nisser, 2016-07-08

# THIS SCRIPT SHOULD RUN ON PYTHON 3!
# ****************************** #
# https://dev.twitter.com/rest/reference/get/followers/ids

from tweepy import OAuthHandler
import json
import time
from tweepy.streaming import StreamListener
from tweepy import Stream
from sys import platform
import config # local config file to store password and user keys etc.

print("Started running script 02_bosnian_users.py at %s" % time.ctime())

counter = 0
# ****************************************** #
# Define keyword track list:
# Read in keyword list from the three files (100 most common
# Bosnian, Serbian and Croatian words:
keyword_list = [] #track list
#
languages =  ['bs', 'hr', 'sr']
#
for language in languages:
	name = ''.join(['100mostcommon_', language, '.txt'])
	text_file = open(name, "r")
	words = text_file.readlines()
	words = [word[:-1] for word in words]
	if keyword_list:
		keyword_list.append(words) # when keyword list is no longer empty
		# print(language)
	else: # when keyword list is still empty
		keyword_list = words
		# print(language)
	# print(keyword_list)
	text_file.close()

# Flatten the nested list:
keyword_list = [val for sublist in keyword_list for val in sublist]

# Use (potential duplicate) words only once:
keyword_list =list(set(keyword_list))


# Add election words:

elections = ['stranka', 'stranke', 'bih', 'bosna', 'bosne', 'rs', 'izboribih', 'izbori',
			 'sdpbih', 'sda', 'sbb_bih', 'dnz', 'asdabih', 'asda', 'bihhdz', 'hdz', 'zabih',
			 'hsp', 'hspbih', 'radomzaboljitak', 'SNSDDodik', 'Dodik', 'СНСД', 'snsd',
			 'СДС', 'sdsrs', 'sdsrs.com ', 'Насловна', 'РС', 'ПДП', 'PDP_RSrpska',
			 'srpskaRS', 'Српска', 'Радикална',  'Странка', 'vlada']

keyword_list +=  elections # combine elections and keyword list.

# ****************************************** #
# Define the place of the document depending on whether the script
# runs on the local machine or on the server:
if platform == "darwin":
	doc_path = '/Users/Annerose/Documents/15-16/Data/bs_all_tweets.txt'
if platform == "linux" or platform == "linux2":
	doc_path = '/home/annerose/Python/bs_all_tweets.txt'

# ****************************************** #
try: # if file is already existent
	with open(doc_path, 'a+') as f:
		# Delete last "\n" and last ","
		f.seek(0, 2)  # set curser from beginning to end.
		size = f.tell()  # tell the length of the file.
		f.truncate(size - 1)  # truncate to this length.

		f.write(u',\n') # add comma  and newline after last tweet from file.


except: # if file doesn't exist, create it and add "[" at the very beginning.
	with open(doc_path, 'a+') as f:
		f.write(u'[')
# ****************************************** #

# Get the Twitter keys
ckey = config.ckey
consumer_secret = config.consumer_secret
access_token_key = config.access_token_key
access_token_secret = config.access_token_secret


auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)

# ****************************************** #

class listener(StreamListener):

	def on_data(self, data):
		global counter

		# data is of type str, so it has to be transformed to a dict:
		data = json.loads(data)
		# print(type(data))
		# subset the dict (use only certain parts of the tweet):
		keys = ['screen_name', 'name', 'user_id', 'location',
				'time_zone', 'profile_created_at',
				'friends_count', 'followers_count',
				'favourites_count',
				'user_lang',
				'text', 'id_str',
				'tweet_created_at', 'tweet_lang']
		tweet = dict.fromkeys(keys)
		tweet['screen_name'] = data['user']['screen_name']
		tweet['name'] = data['user']['name']
		tweet['user_id'] = data['user']['id']
		tweet['location'] = data['user']['location']
		tweet['time_zone'] = data['user']['time_zone']
		tweet['profile_created_at'] = data['user']['created_at']
		tweet['friends_count'] = data['user']['friends_count']
		tweet['followers_count'] = data['user']['followers_count']
		tweet['favorites_count'] = data['user']['favourites_count']
		tweet['user_lang'] = data['user']['lang']

		tweet['text'] = data['text']
		tweet['id_str'] = data['id_str']
		tweet['tweet_created_at'] = data['created_at']
		tweet['tweet_lang'] = data['lang']
		print(tweet)

		excluded_locs = ['Macedonia'] # don't write tweets from excluded_locs to file.
		if tweet['location'] not in excluded_locs:
			with open(doc_path, 'a+') as outfile:
				json.dump(tweet, outfile)
				outfile.write(u',\n')  # add newline
				print("Wrote new tweet to file (user %s)" % tweet['screen_name'])
				counter +=1
				print(counter)

	def on_error(self, status):
			print(status)

# ****************************************** #

try:
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=keyword_list,  # follow = tweeters,
						 languages=['bs', 'hr', 'sr'],
						 locations=[15.5, 42.4, 19.5, 45.4]) # Locations within Bosnia,
	# use Bosnian longitudes and latitudes.

	# Print every 10 minutes the number of new tweets to terminal:
	print("Wrote %d new tweeters to file" % counter)


except KeyboardInterrupt:
	with open(doc_path, 'a+') as f:
		# Delete last "\n" and last ","
		f.seek(0, 2)  # set curser from beginning to end.
		size = f.tell()  # tell the length of the file.
		f.truncate(size - 2)  # truncate to this length (remove last two characters).

		# Add last "]"
		f.write(u']')
		# Close file.

# ****************************************** #
# What to do when the document is shutting down (normally,
# without keyboard interrupt):
with open(doc_path, 'a+') as f:
	# Delete last "\n" and last ","
	f.seek(0, 2)  # set curser from beginning to end.
	size = f.tell()  # tell the length of the file.
	f.truncate(size - 2)  # truncate to this length (remove last two characters).

	# Add last "]"
	f.write(u']')
	# Close file.