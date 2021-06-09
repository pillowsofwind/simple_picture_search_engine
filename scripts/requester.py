import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import tqdm
import json
import requests

f = open("data_test.json", "r")
obj_list = json.loads(f.read())

def generate_actions():
	global obj_list
	for o in obj_list:
		o["_id"] = o["ID"]
		yield(o)

server = Elasticsearch("http://localhost:9200")
print(server.count())

# upload data

for ok, action in streaming_bulk(client=server, index="images", actions=generate_actions()):
	pass

print(server.count())