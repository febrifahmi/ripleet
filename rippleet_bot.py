# This Python file uses the following encoding: utf-8
'''

:::=== Rippleet v.0.1 ===:::
Written by: @febrifahmi (adapted from many sources)
@rippleet will responds to mentions and reply it with social media analytics summary

'''
from bs4 import BeautifulSoup, CData
from datetime import datetime, timedelta
import bs4
import functions as fn
import logging
import os
import time
import json
import re
import requests
import settings
import sqlite3
from urllib3.exceptions import ProtocolError, TimeoutError, SSLError, ReadTimeoutError, ConnectionError, IncompleteRead

# read width and height of the terminal window
(width, height) = fn.getTerminalSize()

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

'''
Request format: " @rippleet search "text you want to search" "
'''

'''
Karena sulitnya mendapatkan API key, kita coba dengan scraping teknik:

1. URL untuk search latets twit: https://mobile.twitter.com/search?q=%s&src=typed_query" %(searchterm)

	q= merupakan lokasi search query nya. kita menggunakan mobile.twitter.com since twitter.com is seem harder to handle

2. pencarian bisa menggunakan beautifulsoup (infinite scroll scraping)

'''

# set search term
searchterm = 'wisata'
operator = ''
lang = 'id'
dbfile = "../" + "%s_%s" %(searchterm, fn.getdatetimenow()) + ".sqlite"

# [3] set url and initiate bautifulsoup parser object
# urltoparse = "https://twitter.com/search?q=%s" %(searchterm)
baseurl = "https://mobile.twitter.com"
starturl = "https://mobile.twitter.com/search?l=%s&q=%s&src=typed_query" %(lang, searchterm+" "+operator)
nexturltoparse = ""

countpage = 0

def setupSqliteDB():
	# connect to sqlite3 database
	conn = sqlite3.connect(dbfile)
	# create cursor object and execute CREATE TABLE
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS tweetdata (username VARCHAR, fullname VARCHAR, avatar VARCHAR, tweet TEXT, links TEXT, hashtags VARCHAR, published TEXT)')
	cur.execute('DELETE FROM tweetdata')
	conn.commit()
	conn.close()

def checkNextPage(soup):
	global countpage
	loadmore = soup.find("div",{"class":"w-button-more"})
	if loadmore:
		nextpage = loadmore.find("a",href=True)
		if nextpage:
			nextpage_url = nextpage['href']
			nexturltoparse = baseurl+nextpage_url
			countpage = countpage+1
			return nexturltoparse,countpage
	else:
		print "No more page. Finished!"
		print(soup)
		exit()

def collectItems(url,nexturl):
	fn.ToRify()
	if len(nexturl) == 0:
		response = requests.get(url)
	else:
		response = requests.get(nexturl)
	# initiating bs4 object parser
	html_soup = BeautifulSoup(response.text, 'html.parser')
	# print html_soup

	# [4] parse the result
	tweet_container = html_soup.select("table.tweet")
	# print tweet_container
	
	counter = 0

	try:
		for item in tweet_container:
			if item is not None:
				item_username = item.find("div",{"class":"username"}).get_text().strip()
				item_avatar = item.find("td",{"class":"avatar"}).find("img")['src']
				item_fullname = item.find("strong",{"class":"fullname"}).get_text().strip()
				item_text = re.sub(r'[(\r\n|\r|\n\r)+]', "", item.find("div",{"class":"tweet-text"}).get_text().strip())
				if item.find("a",{"class":"twitter_external_link dir-ltr tco-link"}):
					item_external_link = item.find("a",{"class":"twitter_external_link dir-ltr tco-link"})['data-expanded-url']
				else:
					item_external_link = "(No link)"
				if item.find("a",{"class":"twitter-hashtag dir-ltr"}):
					item_hashtags = item.find("a",{"class":"twitter-hashtag dir-ltr"}).get_text()
				else:
					item_hashtags = "(No hashtags)"
				if item.find("td",{"class":"timestamp"}):
					item_deltatime = item.find("td",{"class":"timestamp"}).get_text()
					print item_deltatime
					if re.search(r'(\d+h)',item_deltatime):
						deltahours = int(re.search(r'(\d+)',item_deltatime).group(0))
						item_publish_time = datetime.now()-timedelta(hours=deltahours)
						print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
					elif re.search(r'(\d+m)',item_deltatime):
						deltaminutes = int(re.search(r'(\d+)',item_deltatime).group(0))
						item_publish_time = datetime.now()-timedelta(minutes=deltaminutes)
						print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
					elif re.search(r'(\d+s)',item_deltatime):
						deltaseconds = int(re.search(r'(\d+)',item_deltatime).group(0))
						item_publish_time = datetime.now()-timedelta(seconds=deltaseconds)
						print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
					else:
						if len(str(item_deltatime).strip().split()) > 2:
							if datetime.strptime(str(item_deltatime).strip(), "%b %d %y"):
								item_publish_time = datetime.strptime(str(item_deltatime).strip(), "%b %d %y")
								print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
							elif datetime.strptime(str(item_deltatime).strip(), "%d %b %y"):
								item_publish_time = datetime.strptime(str(item_deltatime).strip(), "%d %b %y")
								print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
							else:
								pass
						elif len(str(item_deltatime).strip().split()) == 2:
							if datetime.strptime(str(item_deltatime).strip(), "%b %d"):
								item_publish_time = datetime.strptime(str(item_deltatime+" "+str(datetime.today().year)).strip(), "%b %d %Y")
								print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
							else:
								pass
						else:
							pass
						# if datetime.strptime(str(item_deltatime).strip(), "%b %d"):
						# 	item_publish_time = datetime.strptime(str(item_deltatime+" "+str(datetime.today().year)).strip(), "%b %d %Y")
						# 	print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
						# elif datetime.strptime(str(item_deltatime).strip(), "%b %d %y"):
						# 	item_publish_time = datetime.strptime(str(item_deltatime).strip(), "%b %d %y")
						# 	print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
						# elif datetime.strptime(str(item_deltatime).strip(), "%d %b %y"):
						# 	item_publish_time = datetime.strptime(str(item_deltatime).strip(), "%d %b %y")
						# 	print item_publish_time.strftime("%a, %d %b %Y %I:%M:%S")
						# else:
						# 	pass
				
				print "Tweet data --> %s: %s |--| %s |--| %s |--| %s |--| %s" % (item_username, item_text, item_external_link, item_hashtags, item_avatar, item_publish_time)
				counter = counter+1

				try:
					conn = sqlite3.connect(dbfile)
					cur = conn.cursor()
					cur.execute('INSERT INTO tweetdata (username, fullname, avatar, tweet, links, hashtags, published) VALUES (?,?,?,?,?,?,?);',(item_username,item_fullname,item_avatar,item_text,item_external_link,item_hashtags,item_publish_time))
					conn.commit()
					conn.close()
					print "========>>> Successfully insert data into database! <<<========"
					print "_"*width

				except Exception as ex:
					print("Cannot insert data: ", str(ex))
			else:
				pass

	except Exception as ex:
		print('Error: ',str(ex))
		pass

	loadoldertweet = checkNextPage(html_soup)
	print "Successfully processed %d page(s)." %(countpage)
	time.sleep(5)
	collectItems("",loadoldertweet[0])

if __name__ == "__main__":
	setupSqliteDB()
	try:
		collectItems(starturl,nexturltoparse)
	except (TimeoutError, SSLError, ReadTimeoutError, ConnectionError, IncompleteRead) as e:
		logging.warning("Network error occurred. Keep calm and carry on.", str(e))
		time.sleep(60)
		pass