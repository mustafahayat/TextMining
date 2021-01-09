# import necessary modules
from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# connect to mongo and desired database
try:
   client = MongoClient('localhost',27017)
   db = client.afghanistan
   print("Connected successfully!!!")
except:  
   print("Could not connect to MongoDB")
   
# connect kafka consumer to desired kafka topic	
# consumer = KafkaConsumer('twitterstream_nl',
consumer =  KafkaConsumer("afghanistan", group_id = "afghanistan-group", auto_offset_reset='earliest', bootstrap_servers = ['localhost:9092'])
   # consumer = KafkaConsumer('afghanistan',
   #bootstrap_servers=['localhost:9092'])#,auto_offset_reset='smallest')

# parse desired fields of json twitter object  
for msg in consumer:
    #print(msg)

    # print(msg.value.decode('utf-8'));

    record = json.loads(msg.value.decode('utf-8'))
    text = record['text']
    senti_val = record['senti_val'][:4]
    subjectivity = record['subjectivity'][:4]
    creation_datetime = record['creation_datetime']
    username = record['username']
    location = record['location']
    user_description = record['userDescr']
    followers = record['followers']
    retweets = record['retweets']
    favorites = record['favorites']

    # create dictionary and ingest data into mongo
    try:
       twitter_rec = {'text':text,'senti_val':senti_val,'subjectivity':subjectivity,'creation_datetime':creation_datetime,'username' :username,'location':location,
                      'user_description':user_description,'followers':followers,'retweets':retweets,'favorites':favorites}
       rec_id1 = db.tweets_info.insert_one(twitter_rec)
       print("Data inserted with record ids",rec_id1)
    except:
       print("Could not insertInMongo")
