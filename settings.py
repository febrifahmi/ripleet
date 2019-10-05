# This Python file uses the following encoding: utf-8
# This is the file where the configuration for rippleet.py comes from

# Setup Terms
with open('../terms/trackterms.txt','r') as trackterms:
	TRACK_TERMS = trackterms.read().splitlines()
with open('../terms/badterms.txt','r') as badterms:
	BAD_TERMS = badterms.read().splitlines()
with open('../terms/blockterms.txt','r') as blockterms:
	BLOCK_TERMS = blockterms.read().splitlines()
# Setup lang filter
LANGUAGE_FILTER = ["in"]
# Setup keys
with open('../key/consumerkey.txt','r') as conskey:
	CONSUMER_KEY = conskey.read().replace('\n', '')
with open('../key/consumersecret.txt','r') as conssec:
	CONSUMER_SECRET = conssec.read().replace('\n', '')
with open('../key/accesstoken.txt','r') as acctok:
	ACCESS_TOKEN = acctok.read().replace('\n', '')
with open('../key/accesstokensecret.txt','r') as acctoksec:
	ACCESS_TOKEN_SECRET = acctoksec.read().replace('\n', '')
# Setup Database access
with open('../key/dbuser.txt','r') as dbuser:
	RIPPLEET_USER = dbuser.read().replace('\n', '')
with open('../key/dbpass.txt','r') as dbpass:
	RIPPLEET_PASS = dbpass.read().replace('\n', '')
# Setup PostgreSQL
PSQL_HOST = 'localhost'
PSQL_PORT = 5432
with open('../key/psqldb.txt','r') as psqldb:
	PSQL_DB = psqldb.read().replace('\n', '')
# Setup TCP/IP
TCP_IP = "localhost"
TCP_PORT = 31337