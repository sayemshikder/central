#!/usr/bin/env python
"""Utility script to add a new authorized host."""


import logging
import pymongo
import argparse
import datetime

logging.basicConfig()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('hostname', help='hostname to be added to authd instances')
arg_parser.add_argument('--db_uri', help='DB uri', default='mongodb://127.0.0.1/central')
args = arg_parser.parse_args()

log = logging.getLogger('add_host')

kwargs = dict(tz_aware=True)
db_client = pymongo.MongoReplicaSetClient(args.db_uri, **kwargs) if 'replicaSet' in args.db_uri else pymongo.MongoClient(args.db_uri, **kwargs)
db = db_client.get_default_database()

# is there already a host entry for this hostname?
if not db.instances.find_one({'_id': args.hostname}):
    db.instances.insert({'_id': args.hostname, 'date_added': datetime.datetime.now()})
    log.info('entry created for host %s' % args.hostname)
else:
    log.info('entry already exists for host %s' % args.hostname)
