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
    credentialDict = {"trevor.latson@gmail.com":    "calendar_trevor.dat",
                      "zachbwhaley@gmail.com":     "calendar_zach.dat" }

    if calendarId not in credentialDict:
        print "WARNING: Could not find credentials file for: ", calendarId
        exit(1)

#     here = os.path.dirname(os.path.realpath(__file__))
#     storage_file = os.path.join(here, credentialDict[calendarId])
#     #print "The certificate file is: " , storage_file
#     storage = Storage(storage_file)
#     credentials = storage.get()

#Hard-Code the credentials for testing purposes

    credentials = {"_module": "oauth2client.client",
                   "token_expiry": "2013-11-27T00:49:47Z", 
                   "access_token": "ya29.1.AADtN_XrfHqEfea1WC8mS8X5p-SShhlG8WxvpAgIxcyK6rryi1DyMnkumDKe7uI", 
                   "token_uri": "https://accounts.google.com/o/oauth2/token", 
                   "invalid": false, 
                   "token_response": {"access_token": "ya29.1.AADtN_XrfHqEfea1WC8mS8X5p-SShhlG8WxvpAgIxcyK6rryi1DyMnkumDKe7uI",
                                      "token_type": "Bearer", 
                                      "expires_in": 3600, 
                                      "refresh_token": "1/YIBRJZS-eme2HnUnhit3De3UDTaZbIFyBBliKL2WuR8"}, 
                   "client_id": "776144896653-ovs0rpdv5pus34kp0ppdor59aq6je7u7.apps.googleusercontent.com", 
                   "id_token": null, 
                   "client_secret": "vqezEV9dGDzvjYBm-pfkI718", 
                   "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", 
                   "_class": "OAuth2Credentials", 
                   "refresh_token": "1/YIBRJZS-eme2HnUnhit3De3UDTaZbIFyBBliKL2WuR8", 
                   "user_agent": "xxxxxxxx/vXX"}
   
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
