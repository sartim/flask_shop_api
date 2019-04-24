import os, re, logging
from elasticsearch import Elasticsearch
import certifi

elasticsearch = None

if os.environ.get('ES_URL'):
    # Log transport details (optional):
    logging.basicConfig(level=logging.INFO)

    # Parse the auth and host from env:
    bonsai = os.environ.get('ES_URL')
    auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

    # Connect to cluster over SSL using auth for best security:
    es_header = [{
     'host': host,
     'port': 443,
     'use_ssl': True,
     'http_auth': (auth[0],auth[1]),
     'ca_certs': certifi.where()
    }]

    # Instantiate the new Elasticsearch connection:
    elasticsearch = Elasticsearch(es_header)

    # Verify that Python can talk to Bonsai (optional):
    elasticsearch.ping()