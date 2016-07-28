from pymongo import MongoClient
import json


def install(stoplist=None):
    client = MongoClient()
    db = client.manhattan_project
    topics_collection = db.topics
    topics_collection.remove()
    topics_collection.create_index("topic")

    with open('physics_topics.json', 'r') as infile:
        topics = json.load(infile)
    for topic in topics:
        topic["topic"] = topic["topic"].lower()
        if stoplist:
            topic["topic"] = ' '.join([word for word in topic["topic"].split(' ') if word not in stoplist])
    topics_collection.insert_many(topics)

if __name__ == "__main__":
    with open('SmartStoplist.txt','r') as stopfile:
        stoplist = stopfile.read().splitlines()[1:]

    install(stoplist=stoplist)
