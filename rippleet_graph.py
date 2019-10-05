# This Python file uses the following encoding: utf-8
'''
:::=== Rippleet v.0.1 ===:::
Written by: @febrifahmi (adapted from many sources)
This code analyze data and present SNA analysis as graph network visualization using NetworkX 
'''
import json
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from elasticsearch import Elasticsearch

# [1] Read data from elasticsearch into pandas dataframe. we filter directly the hits.hits.* content ex: http://localhost:9200/rippleet_tweet/_search?q=idul+fitri&size=5000&filter_path=hits.hits.*&pretty
# change to:     _search?q=_exists_:retweeted_status%20AND%20lebaran    <-- to filter data and return only tweet which has retweeted_status key and contains word "lebaran"
searchQuery = "_exists_:retweeted_status+AND+lebaran"
urltoload = "http://localhost:9200/rippleet_tweet/_search?q=%s&size=1000&filter_path=hits.hits.*&pretty" % (searchQuery)
df = pd.read_json(path_or_buf=urltoload) 

# debug
# for x in df['hits']:
#     for item in x:
#         if 'extended_tweet' in item['_source']:
#             print item['_source']['user']['screen_name'] + ": " + item['_source']['extended_tweet']['full_text']
#         else:
#             print item['_source']['user']['screen_name'] + ": " + item['_source']['text']
#         print "------------------------------------------------"

# [2] Initialize Graph from pandas edgelist (undirected) object; see manual --> Graph() = undirected; DiGraph() = directed; MultiGraph() = multiple undirected; MultiDiGraph() = directed version of MultiGraph()
newdf = pd.DataFrame()
for x in df['hits']:
    newdf['node1'] = [y['_source']['user']['screen_name'] for y in x]
    newdf['node2'] = [y['_source']['in_reply_to_screen_name'] for y in x]
    newdf['rtcount'] = [y['_source']['retweet_count'] for y in x]
newdf.head(10)

G=nx.from_pandas_edgelist(newdf,source='node1',target='node2',edge_attr='rtcount')
G.nodes()
G.edges()

# draw the result
plt.figure(figsize=(14,14))
nx.draw_networkx(G, node_size=3, node_color='b', edge_weight='0.1', edge_color='grey', with_labels=True)
plt.show()