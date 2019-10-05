# Adapted from Laurent Weichberger's and friends code (Hortonworks, RAND Corp)
# This script use Apache Spark.
# This code was designed to be run as: spark-submit SparkDemo.py
import time
import json
import settings
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
 
# Set up Spark context
sc = SparkContext("local[2]", "Rippleet")
ssc = StreamingContext(sc, 5) #5 is the batch interval in seconds
IP = settings.TCP_IP
Port = settings.TCP_PORT
lines = ssc.socketTextStream(IP, Port)
 
# When your DStream (discretized stream) in Spark receives data, it creates an RDD every batch interval.
# We use coalesce(1) to be sure that the final filtered RDD has only one partition,
# so that we have only one resulting part-00000 file in the directory.
# The method saveAsTextFile() should really be re-named saveInDirectory(),
# because that is the name of the directory in which the final part-00000 file is saved.
# We use time.time() to make sure there is always a newly created directory, otherwise
# it will throw an Exception.

# untuk sementara data tidak disave sebagai RDD untuk menghemat space, data hanya disave di PostgreSQL DB dan juga diindex di Elasticsearch, untuk save data RDD, uncomment baris dibawah ini
lines.foreachRDD( lambda rdd: rdd.coalesce(1).saveAsTextFile("../tweets/%f" % time.time()) )

#You must start the Spark StreamingContext, and await process termination
ssc.start()
ssc.awaitTermination()