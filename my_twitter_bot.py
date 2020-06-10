import tweepy
import time
# NOTE: I put my keys in the keys.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.
from secrets import *
from web_scraper import *

# NOTE: flush=True is just for running this script
# with PythonAnywhere's always-on task.
# More info: https://help.pythonanywhere.com/pages/AlwaysOnTasks/
print('this is my twitter bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        try:
            print(str(mention.id) + ' - ' + mention.full_text, flush=True)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, FILE_NAME)
            if '#COVID19KE' in mention.full_text.upper():
                print('found #COVID19KE', flush=True)
                print('responding back...', flush=True)

                with open('tweet.txt', 'r') as f:
                    api.update_status('@' + mention.user.screen_name +
                    f.read(), mention.id)
            else:
                 pass  
            
        except tweepy.TweepError as e:
            print(e.reason)       

while True:
    reply_to_tweets()
    time.sleep(15)