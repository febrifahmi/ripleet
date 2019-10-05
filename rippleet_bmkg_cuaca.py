# This Python file uses the following encoding: utf-8
'''
:::=== Rippleet v.0.1 ===:::
Written by: @febrifahmi (adapted from many sources)
This code collects data from antara news online portal and index it to the Elasticsearch 
'''

from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import functions as fn
import logging
import os
import json
import psycopg2
import re
import requests
import settings

# set news portal name
dataname = 'BMKG - Perkiraan Cuaca'
namatable = 'rippleet_bmkg_cuaca'

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

	create_table_q = '''CREATE TABLE IF NOT EXISTS %s (ID SERIAL PRIMARY KEY NOT NULL, NEWSPORTAL TEXT NOT NULL, TITLE TEXT NOT NULL, CONTENT TEXT NOT NULL, NEWSURL TEXT NOT NULL, NEWSTAG TEXT NOT NULL, PUBDATE DATE NOT NULL);''' %(namatable)

	cursor.execute(create_table_q)
	conn.commit()
	print " [+] " + "Table created successfully (or already exists) in PostgreSQL Database: %s" % (settings.PSQL_DB)

except (Exception, psycopg2.DatabaseError) as error :
	print (" [+] Error while creating PostgreSQL table: %s", error) %(namatable)

finally:
	# closing database connection.
    if(conn):
        cursor.close()
        conn.close()
        print " [+] PostgreSQL connection is closed"

# [2] now trying to connect to Elasticsearch and create the index
nameofindex = "rippleet_bmkg_cuaca"
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
urltoparse = ["http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Aceh.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Bali.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-BangkaBelitung.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Banten.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Bengkulu.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-DIYogyakarta.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Gorontalo.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Jambi.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-JawaBarat.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-JawaTengah.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-KalimantanBarat.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-KalimantanSelatan.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-KalimantanTengah.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-KalimantanTimur.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-KalimantanUtara.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-KepulauanRiau.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Lampung.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Maluku.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-MalukuUtara.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-NusaTenggaraBarat.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-NusaTenggaraTimur.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Papua.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-PapuaBarat.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Riau.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SulawesiBarat.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SulawesiSelatan.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SulawesiTengah.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SulawesiTenggara.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SulawesiUtara.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SumateraBarat.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SumateraSelatan.xml",
				"http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-SumateraUtara.xml"]
				# "http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-Indonesia.xml"

# processing the url one by one
for urlitem in urltoparse:
	response = requests.get(urlitem)
	tree = ET.fromstring(response.text)
	for data in tree:
		for area in data.findall('area'):
			# print(area.tag,area.attrib)
			for parameter in area.findall('parameter'):
				if parameter.attrib['id'] == 'hu':					# only extract humidity parameter
					area_name = area.attrib['description']
					area_prov = area.attrib['domain']
					area_lat = area.attrib['latitude']
					area_lon = area.attrib['longitude']
					parameter_title_hu = parameter.attrib['description']
					parameter_hu_data = {timerange.attrib['h']: timerange.find('value').text for timerange in parameter}
					hu_pukul0 = parameter_hu_data.get('0')
					hu_pukul6 = parameter_hu_data.get('6')
					hu_pukul12 = parameter_hu_data.get('12')
					hu_pukul18 = parameter_hu_data.get('18')
					hu_pukul24 = parameter_hu_data.get('24')
					hu_pukul30 = parameter_hu_data.get('30')
					hu_pukul36 = parameter_hu_data.get('36')
					hu_pukul42 = parameter_hu_data.get('42')
					hu_pukul48 = parameter_hu_data.get('48')
					hu_pukul54 = parameter_hu_data.get('54')
					hu_pukul60 = parameter_hu_data.get('60')
					hu_pukul66 = parameter_hu_data.get('66')
					# unpack the values (let call this value v) in dictionary parameter_hu_data
					# unpacked = parameter_hu_data.iteritems()
					# # for key,v in parameter_hu_data.iteritems():
					# # 	print key + ": " + v
					# pukul0, pukul6, pukul12, pukul18, pukul24, pukul30, pukul36, pukul42, pukul48, pukul54, pukul60, pukul66 = [v for key,v in unpacked]
					print "------------------------------"
					print area_name + " (" + area_prov + "):" + "Lat: " + area_lat + " " + "Lon: " + area_lon + str(parameter_hu_data)
					print "Pukul ke-00: " + hu_pukul0
					print "Pukul ke-12: " + hu_pukul12
					print "Pukul ke-24: " + hu_pukul24
				else:
					pass
				#print(area.attrib['description'],": ",area.attrib['latitude']," (lat)",area.attrib['longitude']," (lon)"," ",parameter.tag,parameter.attrib)
			# for area in properties.findall('area'):
			# 	print(area.text)
			# 	print('======================')
	# print(ET.tostring(tree, encoding='utf8').decode('utf8'))
	