#!/usr/bin/python

client_id='776144896653-ovs0rpdv5pus34kp0ppdor59aq6je7u7.apps.googleusercontent.com'
client_secret='vqezEV9dGDzvjYBm-pfkI718'
user_agent='xxxxxxxx/vXX' 
developerKey='AIzaSyAUjOc38vN2IXAG826qNDKD2Iqf-6GdPlU' 

import os.path
here = os.path.dirname(os.path.realpath(__file__))
storage_file = os.path.join(here, 'calendar.dat')

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id=client_id,
    client_secret=client_secret,
    scope='https://www.googleapis.com/auth/calendar',
    user_agent=user_agent)

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.

def getCertificate():
    storage = Storage(storage_file)
    credentials = storage.get()
    if credentials is None:
      credentials = run(FLOW, storage)
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Refresh the access token if it has expired
    if credentials.access_token_expired == True:
      credentials.refresh(http)

if __name__ == '__main__':
    getCertificate()
    
