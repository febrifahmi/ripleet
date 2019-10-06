# This Python file uses the following encoding: utf-8
'''
:::=== Rippleet v.0.1 ===:::
Written by: @febrifahmi (adapted from many sources)
This code collects data from TwitterStreamingAPI and index it to the Elasticsearch as well as PostgreSQL DB
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

# [1] Initiating connection to PostgreSQL DB and create table
try:
	conn = psycopg2.connect(user=settings.RIPPLEET_USER,
							password=settings.RIPPLEET_PASS,
							host=settings.PSQL_HOST,
							port=settings.PSQL_PORT,
							database=settings.PSQL_DB)
	cursor = conn.cursor()

	create_table_q = '''CREATE TABLE IF NOT EXISTS rippleet_tweet (ID SERIAL PRIMARY KEY NOT NULL, TIMECOL INT NOT NULL, SCREENNAME TEXT NOT NULL, TWEET TEXT NOT NULL, WORDCOUNTS INT NOT NULL, REPLYCOUNTS INT NOT NULL, RETWEETCOUNTS INT NOT NULL, FAVCOUNTS INT NOT NULL, FOLLOWER INT NOT NULL, POLARITY float(2) NOT NULL);'''

	cursor.execute(create_table_q)
	conn.commit()
	print " [+] " + "Table created successfully (or already exists) in PostgreSQL Database: %s" % (settings.PSQL_DB)

except (Exception, psycopg2.DatabaseError) as error :
	print (" [+] Error while connecting and creating PostgreSQL table", error)

finally:
# closing database connection.
    if(conn):
        cursor.close()
        conn.close()
        print " [+] PostgreSQL connection is closed"

# [2] now trying to connect to Elasticsearch and create the index
# to search the indexed data, use: http://localhost:9200/rippleet_tweet/_search?q=extended_tweet.full_text:indonesia  <-- the query used is in apache lucene query format or directly use search terms in query fo full text search
nameofindex = "rippleet_tweet-%s" % (fn.gettodaysdate())
try:
	ok = fn.connect_elasticsearch()
	fn.create_index_tweet(ok, nameofindex)
except Exception as ex:
	print(' [x] Error creating index: ', str(ex))
	traceback.print_exc(file=sys.stdout)

# Set up tweepy strealListener class
class streamListener(StreamListener):

	# def __init__(self, csocket):
	# 	super(StreamListener, self).__init__()
	# 	self.client_socket = csocket

	def on_data(self, data):
	 	(width, height) = fn.getTerminalSize()
	 	objects = []
	 	try:
	 		# split each line of data
	 		objects = data.splitlines()
	 		# objects = re.split(r"[~\r\n]+", data)
	 		for line in objects:
	 			#print type(line)
	 			# loads the data into json object
	 			d = json.loads(line)
		 		# processing the data
		 		if d["lang"] == "id" or d["lang"] == "in":
			 		if 'extended_tweet' in d and 'RT @' not in d['extended_tweet']['full_text']:
			 			teks_twit = re.sub(r'[^a-zA-Z0-9_@ ,.-:/]', '', d['extended_tweet']['full_text'])
			 			teksclean = fn.multiwordReplace(teks_twit,fn.wordDic)
			 			#print teksclean
			 			print console_colors.OKBLUE + d['user']['screen_name'] + ": " + console_colors.ENDC + teksclean + "\n"
				 		print("GMT: "+console_colors.WHITE+time.strftime("%a, %d %b %Y %I:%M:%S GMT"+console_colors.ENDC, time.gmtime()))
				 		print("Local: "+console_colors.WHITE+strftime("%a, %d %b %Y %I:%M:%S %p %Z (GMT+7)\r"+console_colors.ENDC))
				 		# send data to socket for processing in spark
				 		print d['user']['screen_name']
				 		analisis = textblob.TextBlob(d['extended_tweet']['full_text'])
				 		an = analisis.translate(from_lang="id", to="en")
				 		print(an.sentiment)
				 		print(an.polarity)
				 		# self.client_socket.send(data)
				 		# indexing data to Elasticsearch
				 		try:
					 		ok = fn.connect_elasticsearch()
					 		fn.create_index_tweet(ok, nameofindex)
					 		fn.store_record(ok, nameofindex, d)
					 	except Exception as ex:
					 		print('Error creating index: ', str(ex))
					 		traceback.print_exc(file=sys.stdout)
					 		
					 	# insert record to PostgreSQL table
				 		try:
				 			conn = psycopg2.connect(user=settings.RIPPLEET_USER,password=settings.RIPPLEET_PASS,host=settings.PSQL_HOST,port=settings.PSQL_PORT,database=settings.PSQL_DB)
				 			cursor = conn.cursor()
							# insert data into table
							sqlquery = ''' INSERT INTO rippleet_tweet (TIMECOL, SCREENNAME, TWEET, WORDCOUNTS, REPLYCOUNTS, RETWEETCOUNTS, FAVCOUNTS, FOLLOWER, POLARITY) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
							cursor.execute(sqlquery, (fn.gettimeNow(),d['user']['screen_name'], teksclean, len(d['extended_tweet']['full_text'].split()), d['reply_count'], d['retweet_count'], d['favorite_count'], d['user']['followers_count'], an.polarity))
							conn.commit()
							count = cursor.rowcount
							print (count, " Record inserted successfully into table")
						except (Exception, psycopg2.Error) as error:
							if(conn):
								print("Failed to insert record into table", error)
						finally:
							#closing database connection.
							if(conn):
								cursor.close()
								conn.close()
								print(" [*] PostgreSQL connection is closed")
						print console_colors.GREY+ "_" * width + console_colors.ENDC

			 		elif 'extended_tweet' not in d and 'RT @' not in d['text']:
			 			teks_twit = re.sub(r'[^a-zA-Z0-9_@ ,.-:/]', '', d['text'])
			 			teksclean = fn.multiwordReplace(teks_twit,fn.wordDic)
			 			#print teksclean
			 			print console_colors.OKBLUE + d['user']['screen_name'] + ": " + console_colors.ENDC + teksclean + "\n"
				 		print("GMT: "+console_colors.WHITE+time.strftime("%a, %d %b %Y %I:%M:%S GMT"+console_colors.ENDC, time.gmtime()))
				 		print("Local: "+console_colors.WHITE+strftime("%a, %d %b %Y %I:%M:%S %p %Z (GMT+7)\r"+console_colors.ENDC))
				 		# send data to socket for processing in spark
				 		print d['user']['screen_name']
				 		analisis = textblob.TextBlob(d['text'])
				 		an = analisis.translate(from_lang="id", to="en")
				 		print(an.sentiment)
				 		print(an.polarity)
				 		# self.client_socket.send(data)
				 		# indexing data to Elasticsearch
				 		try:
					 		ok = fn.connect_elasticsearch()
					 		fn.create_index_tweet(ok, nameofindex)
					 		# create_index(ok, "rippleet_tweet")
					 		fn.store_record(ok, nameofindex, d)
					 	except Exception as ex:
					 		print('Error creating index: ', str(ex))
					 		traceback.print_exc(file=sys.stdout)
					 		
					 	# insert record to table
				 		try:
				 			conn = psycopg2.connect(user=settings.RIPPLEET_USER,password=settings.RIPPLEET_PASS,host=settings.PSQL_HOST,port=settings.PSQL_PORT,database=settings.PSQL_DB)
				 			cursor = conn.cursor()
							# insert data into table
							sqlquery = ''' INSERT INTO rippleet_tweet (TIMECOL, SCREENNAME, TWEET, WORDCOUNTS, REPLYCOUNTS, RETWEETCOUNTS, FAVCOUNTS, FOLLOWER, POLARITY) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
							cursor.execute(sqlquery, (fn.gettimeNow(),d['user']['screen_name'], teksclean, len(d['text'].split()), d['reply_count'], d['retweet_count'], d['favorite_count'], d['user']['followers_count'], an.polarity))
							conn.commit()
							count = cursor.rowcount
							print (count, " Record inserted successfully into table")
						except (Exception, psycopg2.Error) as error :
							if(conn):
								print("Failed to insert record into table", error)
						finally:
							#closing database connection.
							if(conn):
								cursor.close()
								conn.close()
								print(" [*] PostgreSQL connection is closed")
						print console_colors.GREY+ "_" * width + console_colors.ENDC
					# capturing tweets which are retweet of other's tweet
			 		else:
			 			teks_twit = re.sub(r'[^a-zA-Z0-9_@ ,.-:/]', '', d['text'])
			 			teksclean = fn.multiwordReplace(teks_twit,fn.wordDic)
			 			#print teksclean
			 			print console_colors.OKBLUE + d['user']['screen_name'] + ": " + console_colors.ENDC + teksclean + "\n"
				 		print("GMT: "+console_colors.WHITE+time.strftime("%a, %d %b %Y %I:%M:%S GMT"+console_colors.ENDC, time.gmtime()))
				 		print("Local: "+console_colors.WHITE+strftime("%a, %d %b %Y %I:%M:%S %p %Z (GMT+7)\r"+console_colors.ENDC))
				 		# send data to socket for processing in spark
				 		print d['user']['screen_name']
				 		analisis = textblob.TextBlob(d['text'])
				 		an = analisis.translate(from_lang="id", to="en")
				 		print(an.sentiment)
				 		print(an.polarity)
				 		# self.client_socket.send(data)
				 		# indexing data to Elasticsearch
				 		try:
					 		ok = fn.connect_elasticsearch()
					 		fn.create_index_tweet(ok, nameofindex)
					 		# create_index(ok, "rippleet_tweet")
					 		fn.store_record(ok, nameofindex, d)
					 	except Exception as ex:
					 		print('Error creating index: ', str(ex))
					 		traceback.print_exc(file=sys.stdout)
					 		pass
					 	# insert record to table
				 		try:
				 			conn = psycopg2.connect(user=settings.RIPPLEET_USER,password=settings.RIPPLEET_PASS,host=settings.PSQL_HOST,port=settings.PSQL_PORT,database=settings.PSQL_DB)
				 			cursor = conn.cursor()
							# insert data into table
							sqlquery = ''' INSERT INTO rippleet_tweet (TIMECOL, SCREENNAME, TWEET, WORDCOUNTS, REPLYCOUNTS, RETWEETCOUNTS, FAVCOUNTS, FOLLOWER, POLARITY) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
							cursor.execute(sqlquery, (fn.gettimeNow(),d['user']['screen_name'], teksclean, len(d['text'].split()), d['reply_count'], d['retweet_count'], d['favorite_count'], d['user']['followers_count'], an.polarity))
							conn.commit()
							count = cursor.rowcount
							print (count, " Record inserted successfully into table")
						except (Exception, psycopg2.Error) as error :
							if(conn):
								print("Failed to insert record into table", error)
						finally:
							#closing database connection.
							if(conn):
								cursor.close()
								conn.close()
								print(" [*] PostgreSQL connection is closed")
						print console_colors.GREY+ "_" * width + console_colors.ENDC 
			 			# delay 2 secs
			 			time.sleep(2)
			 	else:
			 		pass

		except BaseException as e:
			print("Error on_data: %s" % str(e))
			if e.code == 429:
				print "Sleep mode for 5 minutes."
				time.sleep(300)
			else:
				print "Delay for 5 seconds."
				time.sleep(5)

		# record the data into postgresql data
		def on_exception(self, exception):
			print(exception)
			return

		def on_error(self, status):
			print(status)
			return True

# start streaming tweet and send the data to client_socket
def sendData(c_socket):
    stream_listener = streamListener(c_socket)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')
    while True:
        try:
            stream.filter(track=settings.TRACK_TERMS)
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

# start sreaming
def startStream():
	stream_listener = streamListener()
	stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')
	while True:
		try:
			stream.filter(track=settings.TRACK_TERMS)
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


# TO DO: write report to html file

if __name__ == "__main__":
	logging.basicConfig(level=logging.ERROR)
	# s = socket.socket()     	# Create a socket object
	# host = settings.TCP_IP      # Get local machine name
	# port = settings.TCP_PORT    # Reserve a port for your service.
	# s.bind((host, port))    	# Bind to the port

	# print console_colors.OKBLUE + " [+] " + console_colors.ENDC + "Host %s Listening on port: %s" % (host,str(port))

	# s.listen(5)                 # Now wait for client connection.
	# c, addr = s.accept()        # Establish connection with client.

	# print console_colors.OKBLUE + " [+] " + console_colors.ENDC + "Received request from: " + str( addr )

	# sendData(c)
	startStream()