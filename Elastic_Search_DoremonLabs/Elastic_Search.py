# Importing required library

from itertools import count
import logging
from elasticsearch import Elasticsearch
import json
import send_mail
import query
import config as cfg


#configurating logging 
logging.basicConfig(level=logging.INFO,filename='data.log',format='%(asctime)s %(levelname)s-%(message)s')


try:
# Give the elastic search address and authentication
    es = Elasticsearch([cfg.details['host']], http_auth=(cfg.details['user'], cfg.details['passwd']))

except Exception as e:
    logging.exception('Error while fetching information of elastic search')


# Getting all the indices in res

res=es.indices.get_alias(index=cfg.details['index'])
if len(res)==0:
    logging.exception("Error occured while fetching index")


def getindices(index,body):

    """This will return index after searching"""

    return es.search(index=index,body=body)



#total_count_of_timestamp=0
def count_of_doc_in_time_interval(res,body):

    """You are going to calculate the number of documents in given interval of time"""

    total_count_of_timestamp=0
    
    # this code will count the number of file from body
    for name in res:

        data=getindices(name,body)
        for data_timestamp in data['hits']['hits']:

            data_time=data_timestamp['_source']['@timestamp']
            #logging.info("---------------data_time----------------")
            logging.info(data_time)
            total_count_of_timestamp+=1

    logging.info("Total counts in given range of time is--{}".format(total_count_of_timestamp))
    logging.critical("Count for the documents in given time interval is Done!!!")
    return total_count_of_timestamp


# this code will count the number of documents in given range of response time in body1(query)
#total_count_of_response_time=0
def count_of_doc_based_on_response_time(res,body1):

    """You are going to calculate number of documents in given response time"""

    total_count_of_response_time=0
    for name in res:

        data=getindices(name,body1)
        for data_response_time in data['hits']['hits']:

            response_time=data_response_time['_source']['response_time']
            logging.info(response_time)
            total_count_of_response_time+=1

    logging.info("Total Counts in range of response_time<=--{}".format(total_count_of_response_time))
    logging.critical("Count of documents in given range of response time is Done!!!")
    return total_count_of_response_time

#Calling function for count of documents in timestamp
try:
    logging.warning(count_of_doc_in_time_interval.__doc__)
    count_time = count_of_doc_in_time_interval(res,query.body)

except Exception as e:
    logging.exception("Error occured while calculating number of counts")


#Calling function for count of documents in response time
try:
    logging.warning(count_of_doc_based_on_response_time.__doc__)
    count_response = count_of_doc_based_on_response_time(res,query.body1)
except:
    logging.exception("Error occured while calculating number of counts")


def sending_email():

    """You are going to send email"""

    return send_mail.send(count_time,count_response)

try:
    logging.warning(sending_email.__doc__)
    sending_email()
except Exception as e:
    logging.exception("Error while sending email")




