# Importing required library

import logging
from elasticsearch import Elasticsearch
import json
import smtplib

#configurating logging 
logging.basicConfig(filename='data.log',format='%(asctime)s %(levelname)s-%(message)s')

# Storing all details in a variable data from json file
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
logging.critical("Count for the documents in a hour is Done!!!")

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
logging.critical("Count of documents in given range of response time is Done!!!")

#defining a function for sending email

# Creating SMTP Client Session
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security which makes the connection more secure
smtpobj.starttls()
senderemail_id="rudra931592@gmail.com"
senderemail_id_password="password"
receiveremail_id="rudra@doremonlabs.com"
# Authentication for signing to Gmail account
smtpobj.login(senderemail_id, senderemail_id_password)
# message to be sent
message = """From: From Rudra <from@sendermail@gmail.com>
To: To Person <to@receivermail@gmail.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Completion of all Tasks
<h4>Hello sir,</h4>
<p>Please find the below data for this tasks-</p>
<p>Total number of documents in a hour is: {}.</p>
""".format(count_of_timestamp)+"""<p>Total number of documents in given range of response time is: {}.</p>""".format(count_of_response_time)+"<h3>Thanks and Regards</h3>"+"<p>Rudra Pratap Singh</p>"
# sending the mail - passing 3 arguments i.e sender address, receiver address and the message
smtpobj.sendmail(senderemail_id,receiveremail_id, message)
# Hereby terminate the session
smtpobj.quit()
print(" mail send ")
logging.critical('')



