# Importing required library

from elasticsearch import Elasticsearch
import json

with open("cfg.json") as json_data_file:
    data = json.load(json_data_file)

# Give the elastic search address and authentication
es = Elasticsearch([data['details']['host']], http_auth=(data['details']['user'], data['details']['passwd']))
print(es.search(index=data['details']['index'], body={}, size=5))

# Checking for the required index
print(es.indices.exists(index=data['details']['index']))

# Getting all the indices in res
res=es.indices.get_alias(index=data['details']['index'])
for name in res:
   print(name)

# Getting all details of a particular index
ans=es.get(index="quest-staging-apache-accesslogs-2022.02.05",id="0HhHyH4BADqCDtbkZfn0")
print(ans)

# time stamp of a particular index
print(ans['_source']['@timestamp'])

# this query section is for counting the number of documents in a particular range of time range (1 hr) of response code 200.
body={
        'query':{
            'bool':{
                'must':{
                    'match':{
                        "response_code": 200
                    }
                },
                "filter":{
                    "range":{
                        "@timestamp":{
                            "gte":data['details']['start_date_time'],
                            "lte":data['details']['end_date_time']
                        }
                    }
                }
            }
        }
    }

def getindices(index,body):
    return es.search(index=index,body=body)


# this code will count the number of file from body
count_of_timestamp=0
for name in res:
    data=getindices(name,body)
    for data_timestamp in data['hits']['hits']:
        data_time=data_timestamp['_source']['@timestamp']
        print("---------------data_time----------------")
        print(data_time)
        count_of_timestamp+=1
print("Total counts in range of 1 hrs--")
print(count_of_timestamp)

# this query is for counting the documents of response time(100<=response_time<=500) for response_code 500
body1={
        'query':{
            'bool':{
                'must':{
                    'match':{
                        "response_code": 500
                    }
                },
                "filter":{
                    "range":{
                        "response_time":{
                            "gte":100,
                            "lte":500
                        }
                    }
                }
            }
        }
    }

# this code will count the number of documents in given range of response time in body1(query)
count_of_response_time=0
for name in res:
    data=getindices(name,body1)
    for data_response_time in data['hits']['hits']:
        response_time=data_response_time['_source']['response_time']
        print("------------------response_time------------------")
        print(response_time)
        count_of_response_time+=1
print("Total Counts in range of 100<=response_time<=500--")
print(count_of_response_time) 


