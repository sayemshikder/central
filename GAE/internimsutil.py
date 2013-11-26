#!/usr/bin/env python
#
# @author:  Kevin S. Hahn

import base64
import logging
import urllib2
import httplib                      # to deal with httplib.InvalidURL exceptions
import webapp2
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from google.appengine.ext import db
logging.basicConfig(level=logging.INFO)


key_AuthorizedHosts = db.Key.from_path('InterNIMS', 'AuthorizedHosts')
key_NIMSServers = db.Key.from_path('InterNIMS', 'NIMSServers')
key_Challenges = db.Key.from_path('InterNIMS', 'Challenges')


class AuthorizedHost(db.Model):

    _id = db.StringProperty()                       # primary ID will be uuid
    commonname = db.StringProperty()                # for human readability
    pubkey = db.StringProperty(multiline=True)      # security item (may change)
    active = db.BooleanProperty()

    def __str__(self):
        return self._id

    def as_dict(self):
        return {'_id': self._id, 'commonname': self.commonname, 'pubkey': self.pubkey}


class NIMSServer(db.Model):

    _id = db.StringProperty()                       # fixed
    commonname = db.StringProperty()                # fixed
    pubkey = db.StringProperty(multiline=True)      # can be updated
    ipv4 = db.StringProperty()                      # can be updated
    hostname = db.StringProperty()                  # can be updated
    timestamp = db.DateTimeProperty()               # may differ every time
    userlist = db.StringListProperty()              # may differ every time

    def __str__(self):
        return '%s: %s' % (str(self.timestamp), self._id)

    def as_dict(self):
        return {'commonname': self.commonname,
                '_id': self._id,
                'ip4': self.ipv4,
                'hostname': self.hostname,
                'pubkey': self.pubkey,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'users': self.userlist}


class CRAMChallenge(db.Model):

    _id = db.StringProperty()
    challenge = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now=True)  # auto_now sets time on put()