from elasticsearch import Elasticsearch
import json

with open("cfg.json") as json_data_file:
    data = json.load(json_data_file)

# Give the elastic search address and authentication
es = Elasticsearch([data['details']['host']], http_auth=(data['details']['user'], data['details']['passwd']))
print(es.search(index=data['details']['index'], body={}, size=5))