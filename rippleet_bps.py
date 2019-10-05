# This Python file uses the following encoding: utf-8
'''
:::=== Rippleet v.0.1 ===:::
Written by: @febrifahmi (adapted from many sources)
This code collects data from BPS web API (https://webapi.bps.go.id/documentation/) and index it to the Elasticsearch as well as PostgreSQL DB
'''
import requests

parameter = {"rel_rhy":"jingle"}
request = requests.get('https://api.datamuse.com/words',parameter)