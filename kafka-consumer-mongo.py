# Import some necessary modules
# pip install kafka-python
# pip install pymongo
# pip install "pymongo[srv]"
from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo.server_api import ServerApi

import json

uri = "mongodb+srv://rodrigomencias08:o8Nl0JitEmFTB6YB@cluster0.7ipkl3j.mongodb.net/?retryWrites=true&w=majority"
# "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.2"


# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

# Connect to MongoDB and pizza_data database

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.peliculas
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

consumer = KafkaConsumer('test',bootstrap_servers=['my-kafka-0.my-kafka-headless.mykafka-lokenmg.svc.cluster.local:9092'])
# Parse received data from Kafka
for msg in consumer:
    record = json.loads(msg.value)
    print(record)
    name = record['name']

    # Create dictionary and ingest data into MongoDB
    try:
       pelicula_rec = {'name':name }
       print (pelicula_rec)
       pelicula_id = db.peliculas_info.insert_one(pelicula_rec)
       print("Data inserted with record ids", pelicula_id)
    except:
       print("Could not insert into MongoDB")
    
    
try:
    ago_result =db.peliculas_info.agregate(
    [{
        "$group" :
        {
            "_id": "$name",
            "n"  : {"$sum" : 1}
        }
    }])
    db.peliculas_sumary.delete_many({})
    for i in agg_result:
        print (i)
        sumary_id = de.peliculas_suamry.insert_one(i)
        print("Sumary inserted with record ids", sumary_id)
except Exception as e:
    print(f'group by caunght {type(e)}: ')
    print(e)
