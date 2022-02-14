# Importing required library

import logging
from elasticsearch import Elasticsearch
import send_email
import query
import config as cfg

# configurating logging
logging.basicConfig(level=logging.INFO, filename='data.log', format='%(asctime)s %(levelname)s-%(message)s')

try:
    # Give the elastic search address and authentication
    es = Elasticsearch([cfg.elastic_search['host']],
                       http_auth=(cfg.elastic_search['user'], cfg.elastic_search['passwd']))

except Exception as e:
    logging.exception('Error while fetching information of elastic search')

# Getting all the indices in res
res = es.indices.get_alias(index=cfg.elastic_search['index'])
if len(res) == 0:
    logging.exception("Error occured while fetching index")


def get_data_of_index(index, body):
    """Return datails of index after matched into the dict.

    Parameters:
    index (str): Index will contain all data of particular index.
    body (tuple): Body is query in which search is apply.

    Returns:
    tuple: After search according to the body in to the index data and then returns"""

    return es.search(index=index, body=body)


def count_of_doc_in_time_interval(res, body):
    """Calculate the number of documents in given interval of time.

    Parameters:
    res (dict): Which include all index into the dict.
    body (tuple): This is query which will pass into get_data_of_index.

    Returns:
    int: Total number of documents in given range of time."""

    total_count_of_timestamp = 0

    for name in res:
        data = get_data_of_index(name, body)
        for data_timestamp in data['hits']['hits']:
            data_time = data_timestamp['_source']['@timestamp']
            logging.info(data_time)
            total_count_of_timestamp += 1

    logging.info("Total counts in given range of time is--{}".format(total_count_of_timestamp))
    return total_count_of_timestamp


def count_of_doc_based_on_response_time(res, body1):
    """Calculate the number of documents in given response of time.

    Parameters:
    res (dict): Which include all index into the dict.
    body1 (tuple): This is query which will pass into get_data_of_index.

    Returns:
    int: Total number of documents in given response of time."""

    total_count_of_response_time = 0
    for name in res:

        data = get_data_of_index(name, body1)
        for data_response_time in data['hits']['hits']:
            response_time = data_response_time['_source']['response_time']
            logging.info(response_time)
            total_count_of_response_time += 1

    logging.info("Total Counts in range of response_time<=- {}".format(total_count_of_response_time))
    return total_count_of_response_time


# Calling function for count of documents in timestamp
try:
    count_time = count_of_doc_in_time_interval(res, query.body)

except Exception as e:
    logging.exception("Error occured while calculating number of counts")

# Calling function for count of documents in response time
try:
    count_response = count_of_doc_based_on_response_time(res, query.body1)
except:
    logging.exception("Error occured while calculating number of counts")

try:
    send_email.send(count_time, count_response)
except Exception as e:
    logging.exception("Error while sending email")