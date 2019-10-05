# This Python file uses the following encoding: utf-8
'''
:::=== Rippleet v.0.1 ===:::
Written by: @febrifahmi (adapted from many sources)
This code collects data from antara news online portal and index it to the Elasticsearch 
'''

from bs4 import BeautifulSoup
import functions as fn
import logging
import os
import json
import psycopg2
import re
import requests
import settings

# set news portal name
newsportalname = 'Antara News'

# read width and height of the terminal window
(width, height) = fn.getTerminalSize()

# [1] Initiating connection to PostgreSQL DB and create table
try:
	conn = psycopg2.connect(user=settings.RIPPLEET_USER,
							password=settings.RIPPLEET_PASS,
							host=settings.PSQL_HOST,
							port=settings.PSQL_PORT,
							database=settings.PSQL_DB)
	cursor = conn.cursor()

	create_table_q = '''CREATE TABLE IF NOT EXISTS rippleet_news (ID SERIAL PRIMARY KEY NOT NULL, NEWSPORTAL TEXT NOT NULL, TITLE TEXT NOT NULL, CONTENT TEXT NOT NULL, NEWSURL TEXT NOT NULL, NEWSTAG TEXT NOT NULL, PUBDATE DATE NOT NULL);'''

	cursor.execute(create_table_q)
	conn.commit()
	print " [+] " + "Table created successfully (or already exists) in PostgreSQL Database: %s" % (settings.PSQL_DB)

except (Exception, psycopg2.DatabaseError) as error :
	print (" [+] Error while creating PostgreSQL table", error)

finally:
	# closing database connection.
    if(conn):
        cursor.close()
        conn.close()
        print " [+] PostgreSQL connection is closed"

# [2] now trying to connect to Elasticsearch and create the index
nameofindex = "rippleet_news"
try:
	ok = fn.connect_elasticsearch()
	fn.create_index_news(ok, nameofindex)
except Exception as ex:
	print(' [x] Error creating index: ', str(ex))
	traceback.print_exc(file=sys.stdout)
	pass

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

# [3] set url and initiate bautifulsoup parser object
urltoparse = "https://www.antaranews.com/rss/terkini"
response = requests.get(urltoparse)
# initiating bs4 object parser
html_soup = BeautifulSoup(response.text, 'lxml')

# [4] parse the result
artikel_container = html_soup.find_all('item')
for item in artikel_container:
	item_judul = item.find('title').get_text()
	item_url = item.find('guid').get_text()
	item_tag = "Terkini"
	item_pubdate = fn.gettodaysdate()
	# print the result
	# print item_judul
	# print item_url
	# print item_tag
	# print item_pubdate
	# print '----------------------------------------'

	# now for each item_url scrape the article content
	try:
		itemresponse = requests.get(item_url)
		content_soup = BeautifulSoup(itemresponse.text, 'html.parser')
		# kill all script and style elements
		for script in content_soup(["script", "style"]):
		    script.decompose()    # rip it out
		konten_container = content_soup.find('article', class_='post-wrapper clearfix').get_text()
	except AttributeError as ex:
		print('Exception: ', str(ex))
		pass
	
	# print konten_container
	# print console_colors.GREY+ "_" * width + console_colors.ENDC

	# # now setup json data for storing in elasticsearch
	data = {}
	data['newstitle'] = item_judul
	data['newsurl'] = item_url
	data['newstag'] = item_tag
	data['newspubdate'] = item_pubdate
	data['newscontent'] = konten_container
	data['newsportal'] = newsportalname
	json_data = json.dumps(data)
	# print json_data

	# # indexing data to Elasticsearch
	try:
 		ok = fn.connect_elasticsearch()
 		fn.store_record(ok, nameofindex, json_data)
 	except Exception as ex:
 		print('Error creating index: ', str(ex))
 		traceback.print_exc(file=sys.stdout)
 		pass

 	# insert record to PostgreSQL table
	try:
		conn = psycopg2.connect(user=settings.RIPPLEET_USER,password=settings.RIPPLEET_PASS,host=settings.PSQL_HOST,port=settings.PSQL_PORT,database=settings.PSQL_DB)
		cursor = conn.cursor()
		# insert data into table
		sqlquery = ''' INSERT INTO rippleet_news (NEWSPORTAL, TITLE, CONTENT, NEWSURL, NEWSTAG, PUBDATE) VALUES (%s,%s,%s,%s,%s,%s) '''
		cursor.execute(sqlquery, (newsportalname, item_judul, konten_container, item_url, item_tag, item_pubdate))
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