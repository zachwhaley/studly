#!/usr/bin/python

client_id='776144896653-ovs0rpdv5pus34kp0ppdor59aq6je7u7.apps.googleusercontent.com'
client_secret='vqezEV9dGDzvjYBm-pfkI718'
user_agent='xxxxxxxx/vXX' 
developerKey='AIzaSyAUjOc38vN2IXAG826qNDKD2Iqf-6GdPlU' 

import os.path
import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS
FLAGS.auth_local_webserver = False


def getService(calendarId):

    # Map calendarId to the certificate file location
    credentialDict = {"nenglish@si2.org":   "calendar_nick.dat",
                      "knesmith@si2.org":   "calendar_kevin.dat",
                      "john.ellis@si2.org": "calendar_john.dat",
                      "jakeb@si2.org":      "calendar_jake.dat",
                      "steve@si2.org":      "calendar_steve.dat",
                      "pfeil@si2.org":      "calendar_barbara_p.dat",
                      "barbarar@si2.org":   "calendar_barbara_r.dat",
                      "parks@si2.org":      "calendar_joanne.dat",
                      "scarver@si2.org":    "calendar_susan.dat",
                      "trevor@si2.org":     "calendar_trevor.dat" }

    if calendarId not in credentialDict:
        print "WARNING: Could not find credentials file for: ", calendarId
        exit(1)

    here = os.path.dirname(os.path.realpath(__file__))
    storage_file = os.path.join(here, credentialDict[calendarId])
    #print "The certificate file is: " , storage_file
    storage = Storage(storage_file)
    credentials = storage.get()
   
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Refresh the access token if it has expired
    if credentials.access_token_expired == True:
        credentials.refresh(http)

    # Build a service object for interacting with the API. Visit
    # the Google APIs Console
    # to get a developerKey for your own application.
    service = build(serviceName='calendar', version='v3', http=http,
           developerKey=developerKey)
    return service
