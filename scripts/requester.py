import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import tqdm
import json
import requests

f = open("data.json", "r")
obj_list = json.loads(f.read())

def generate_actions():
	global obj_list
	for o in obj_list:
		o["_id"] = o["ID"]
		yield(o)

server = Elasticsearch("http://localhost:9200")
print(server.count())

# upload data
if server.count() == 0:
	for ok, action in streaming_bulk(client=server, index="images", actions=generate_actions()):
		pass

print(server.count())

header = {
	"Content-Type": "application/json"
}
settings = {
	"max_result_window": "10000"
}
res = requests.put("http://localhost:9200/images/_settings", headers=header, data=json.dumps(settings))
print(res.json())

# query demo
# while True:
# 	s = input("put a query:")	# query by id
# 	try:
# 		res = server.get("images", s)
# 		print(res)
# 	except:
# 		pass