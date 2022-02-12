# Importing required library

import logging
from elasticsearch import Elasticsearch
import json
import send_mail
import query


#configurating logging 
logging.basicConfig(level=logging.INFO,filename='data.log',format='%(asctime)s %(levelname)s-%(message)s')

# Storing all details in a variable data from json file
with open("cfg.json") as json_data_file:
    data = json.load(json_data_file) 

try:
# Give the elastic search address and authentication
    es = Elasticsearch([data['details']['host']], http_auth=(data['details']['user'], data['details']['passwd']))
    logging.info("Connection successfull!")
except Exception as e:
    logging.exception('Error while fetching information of elastic search')


# Getting all the indices in res
res=es.indices.get_alias(index=data['details']['index'])


def getindices(index,body):
    return es.search(index=index,body=body)


total_count_of_timestamp=0
def count_doc_in_time(res,body):
    global total_count_of_timestamp
    
    # this code will count the number of file from body
    for name in res:

        data=getindices(name,body)
        for data_timestamp in data['hits']['hits']:

            data_time=data_timestamp['_source']['@timestamp']
            #logging.info("---------------data_time----------------")
            logging.info(data_time)
            total_count_of_timestamp+=1

    logging.info("Total counts in given range of time is--")
    logging.info(str(total_count_of_timestamp))
    logging.critical("Count for the documents in given time interval is Done!!!")


# this code will count the number of documents in given range of response time in body1(query)
total_count_of_response_time=0
def count_in_response_time(res,body1):
    global total_count_of_response_time
    for name in res:

        data=getindices(name,body1)
        for data_response_time in data['hits']['hits']:

            response_time=data_response_time['_source']['response_time']
            #logging.info("------------------response_time------------------")
            logging.info(response_time)
            total_count_of_response_time+=1

    logging.info("Total Counts in range of 400<=response_time<=500--")
    logging.info(str(total_count_of_response_time))
    logging.critical("Count of documents in given range of response time is Done!!!")

#Calling function for count of documents in timestamp
count_doc_in_time(res,query.body)

#Calling function for count of documents in response time
count_in_response_time(res,query.body1)

def sending_email():
    send_mail.send(total_count_of_timestamp,total_count_of_response_time)

sending_email()



