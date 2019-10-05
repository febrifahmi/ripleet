# This Python file uses the following encoding: utf-8
'''
:::=== Rippleet v.0.1 ===:::
Written by: @febrifahmi (adapted from many sources)
This code collects data from TwitterStreamingAPI and index it to the Elasticsearch as well as PostgreSQL DB, and report twitter account suspected as fake or spam account
'''

import json
import logging
import os
import psycopg2
import re
import settings
import socket
import sys, traceback
import textblob
import time
import tweepy
import functions as fn
from elasticsearch import Elasticsearch
from psycopg2.extensions import AsIs
from time import gmtime, strftime
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
from urllib3.exceptions import ProtocolError, TimeoutError, SSLError, ReadTimeoutError, ConnectionError, IncompleteRead

# Set authentication for tweepy
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

logfile = "logreport.txt"
# # Report API URL
# reportURLendpoint = "https://api.twitter.com/1.1/users/report_spam.json?"

# Set text console color formatting
class console_colors:
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    FAIL = '\033[91m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    UNDERLINE = '\033[4m'
    WARNING = '\033[93m'
    BLACK = '\033[90m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    DEFAULT = '\033[99m'
    GREEN = '\033[92m'
    GREY = '\033[90m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'

# Set up tweepy strealListener class
class streamListener(StreamListener):

    def on_data(self, data):
        (width, height) = fn.getTerminalSize()
        objects = []
        try:
            # split each line of data
            objects = data.splitlines()
            for line in objects:
                # loads the data into json object
                d = json.loads(line)
                # processing the data .encode('utf-8',errors='ignore')

                if d["lang"] == "id" or d["lang"] == "in":
                    if 'extended_tweet' in d and 'RT @' not in d['extended_tweet']['full_text']:
                        teks_twit = re.sub(r'[^a-zA-Z0-9_@ ,.-:/]', '', d['extended_tweet']['full_text'])
                        teksclean = fn.multiwordReplace(teks_twit,fn.wordDic)
                        # print teksclean
                        # print console_colors.OKBLUE + d['user']['screen_name'].encode('utf-8') + ": " + console_colors.ENDC + teksclean + "\n"
                        # print("GMT: "+console_colors.WHITE+time.strftime("%a, %d %b %Y %I:%M:%S GMT"+console_colors.ENDC, time.gmtime()))
                        # print("Local: "+console_colors.WHITE+strftime("%a, %d %b %Y %I:%M:%S %p %Z (GMT+7)\r"+console_colors.ENDC))
                        # sentiment check
                        analisis = textblob.TextBlob(d['extended_tweet']['full_text'])
                        an = analisis.translate(from_lang="id", to="en")
                        # print(an.sentiment)
                        # print(an.polarity)
                        

                    elif 'extended_tweet' not in d and 'RT @' not in d['text']:
                        teks_twit = re.sub(r'[^a-zA-Z0-9_@ ,.-:/]', '', d['text'])
                        teksclean = fn.multiwordReplace(teks_twit,fn.wordDic)
                        #print teksclean
                        # print console_colors.OKBLUE + d['user']['screen_name'].encode('utf-8') + ": " + console_colors.ENDC + teksclean + "\n"
                        # print("GMT: "+console_colors.WHITE+time.strftime("%a, %d %b %Y %I:%M:%S GMT"+console_colors.ENDC, time.gmtime()))
                        # print("Local: "+console_colors.WHITE+strftime("%a, %d %b %Y %I:%M:%S %p %Z (GMT+7)\r"+console_colors.ENDC))
                        # sentiment check
                        analisis = textblob.TextBlob(d['text'])
                        an = analisis.translate(from_lang="id", to="en")
                        # print(an.sentiment)
                        # print(an.polarity)
                        
                    # capturing tweets which are retweet of other's tweet
                    else:
                        teks_twit = re.sub(r'[^a-zA-Z0-9_@ ,.-:/]', '', d['text'])
                        teksclean = fn.multiwordReplace(teks_twit,fn.wordDic)
                        # print teksclean
                        # print console_colors.OKBLUE + d['user']['screen_name'].encode('utf-8') + ": " + console_colors.ENDC + teksclean + "\n"
                        # print("GMT: "+console_colors.WHITE+time.strftime("%a, %d %b %Y %I:%M:%S GMT"+console_colors.ENDC, time.gmtime()))
                        # print("Local: "+console_colors.WHITE+strftime("%a, %d %b %Y %I:%M:%S %p %Z (GMT+7)\r"+console_colors.ENDC))
                        # sentiment check
                        analisis = textblob.TextBlob(d['text'])
                        an = analisis.translate(from_lang="id", to="en")
                        # print(an.sentiment)
                        # print(an.polarity)

                    for keyword in settings.BLOCK_TERMS:
                        if keyword in teksclean and an.polarity < 0.0:
                            fn.ToRify()
                            print console_colors.WHITE+"Username: "+ console_colors.ENDC +"@%s" %(console_colors.OKBLUE + d['user']['screen_name'] + console_colors.ENDC) + " | " + "Followers= %s" %(str(d['user']['followers_count']))
                            print console_colors.WHITE+"Tweet: "+ console_colors.ENDC + "%s" %(teks_twit)
                            print console_colors.WHITE+"Polarity: "+ console_colors.ENDC + "%s" %(an.polarity)
                            # report account
                            api.report_spam(screen_name=d['user']['screen_name'])
                            print "Keywords %s found in tweet text.. >> " %(keyword) +console_colors.RED+" FOUND"+console_colors.ENDC+" << (Time elapsed: %d)" %(fn.gettimeNow()-starttime)
                            print str(d['user']['screen_name']) + ' is being reported.'
                            print console_colors.GREY+ "_" * width + console_colors.ENDC
                            with open(logfile,'a+') as records:
                                records.write("Reported account: @%s (Follower: %s)" %(d['user']['screen_name'],str(d['user']['followers_count'])) + " | " + "Tweet: %s" %(teks_twit))
                                records.close()

                        else:
                            print console_colors.WHITE+"Username: "+ console_colors.ENDC +"@%s" %(console_colors.OKBLUE + d['user']['screen_name'] + console_colors.ENDC) + " | " + "Followers= %s" %(str(d['user']['followers_count']))
                            print console_colors.WHITE+"Tweet: "+ console_colors.ENDC + "%s" %(teks_twit)
                            print console_colors.WHITE+"Polarity: "+ console_colors.ENDC + "%s" %(an.polarity)
                            print "Keywords %s not found in tweet text.. >> " %(keyword) + console_colors.GREY + "skip"+ console_colors.ENDC +" << (Time elapsed: %d)" %(fn.gettimeNow()-starttime)
                            print console_colors.GREY+ "_" * width + console_colors.ENDC

                    # delay 2 secs
                    time.sleep(2)

                else:
                    pass

        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(0.5)

        # record the data into postgresql data
        def on_exception(self, exception):
            print(exception)
            return

        def on_error(self, status):
            print(status)
            return True

# start sreaming
def startStream():
    stream_listener = streamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')
    while True:
        try:
            stream.filter(track=settings.BAD_TERMS)
            time.sleep(2)
        except (ProtocolError):
            logging.info("Protocol Error.")
            continue
        except (TimeoutError, SSLError, ReadTimeoutError, ConnectionError, IncompleteRead) as e:
            logging.warning("Network error occurred. Keep calm and carry on.", str(e))
            time.sleep(60)
            continue
        finally:
            logging.info("Stream has crashed. System will restart twitter stream!")
            time.sleep(60)

# searching tweet based on keywords list from the stream and return the user.screen_name that tweeting those tweets, filter by number of followers (follower_count)
# if the keyword list found in the tweet, report the user
def searchTwitter():
	queries = ['wan abud']
	for query in queries:
		result = api.search(q=query,count=10000,result_type='mixed')
		return result

def processingTweet():
    print console_colors.GREY+ "=" * width + console_colors.ENDC
    print " "
    print "  Start monitoring tweet stream..."
    print " "
    print console_colors.GREY+ "=" * width + console_colors.ENDC
    startStream()

# TO DO: write report to html file
# start streaming

# processing tweet

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    (width, height) = fn.getTerminalSize()
    starttime = fn.gettimeNow()
    processingTweet()
    # print len(searchTwitter())