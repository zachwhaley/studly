import json
import webapp2
import calendarListUpdate
import calendarCertificate
import os

from google.appengine.ext import ndb
from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

# decorator = OAuth2Decorator(
#   client_id='656176414432-sdq1gmm8csamg9m1ac0u0482gknbhjvh.apps.googleusercontent.com',
#   client_secret='nN6SnG9tZN7LaKQIYZW2J4bA',
#   scope='https://www.googleapis.com/auth/calendar')

decorator = OAuth2DecoratorFromClientSecrets(
  os.path.join(os.path.dirname(__file__), 'client_secret_656176414432.apps.googleusercontent.com.json'),
  scope='https://www.googleapis.com/auth/calendar')

service = build('calendar', 'v3')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Studly")


class GetReflectorList(webapp2.RequestHandler):
    def get(self):          
        reflectorList = "reflectorList1"
        emails = calendarListUpdate.getReflectorList(reflectorList, displayWarning = False) 
        self.response.out.write(json.dumps(emails))
        
class GetCalendarList(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):          
        # Get the authorized Http object created by the decorator.
        http = decorator.http()
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        calendar_list = calendarListUpdate.getCalendarList(calendarId, http) 
        self.response.out.write(json.dumps(calendar_list))
        
class GetEvents(webapp2.RequestHandler):
    def get(self):          
        calendarId = self.request.get('calendarId')
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        events = calendarListUpdate.getEvents(calendarId, pageToken=None) 
        self.response.out.write(json.dumps(events))
        
class GetSingleEvents(webapp2.RequestHandler):
    def get(self):          
        calendarId = self.request.get('calendarId')
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        events = calendarListUpdate.getSingleEvents(calendarId, pageToken=None) 
        self.response.out.write(json.dumps(events))
         
class UpdateEvent(webapp2.RequestHandler):
    def post(self):
        #hard-coded data for testing purposes:
        event = "testEvent1"
        calendarId = "trevor.latson@gmail.com"
        reflectorList = "reflectorList1"
        status = calendarListUpdate.updateEvent(event, calendarId, reflectorList)
        self.response.out.write(status)

        
class UpdateCalendarList(webapp2.RequestHandler):
    def post(self):
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        TimezoneOffset = 0
        status = calendarListUpdate.updateCalendarList(calendarId, TimezoneOffset, debug = True)
        self.response.out.write(status)

        

                
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/reflectors.json', GetReflectorList),
    ('/calendars.json', GetCalendarList),
    ('/events.json', GetEvents),
    ('/single-events.json', GetSingleEvents),
    ('/update-event', UpdateEvent),
    ('/update-calendar', UpdateCalendarList),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
