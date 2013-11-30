import json
import webapp2
import calendarListUpdate
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
    @decorator.oauth_required
    def get(self):          
        # Get the authorized Http object created by the decorator.
        http = decorator.http()
        
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        
        events = calendarListUpdate.getEvents(calendarId, http) 
        self.response.out.write(json.dumps(events))
        
        
class GetSingleEvents(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):          
        # Get the authorized Http object created by the decorator.
        http = decorator.http()
        
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        
        singleEvents = calendarListUpdate.getSingleEvents(calendarId, http) 
        self.response.out.write(json.dumps(singleEvents))
         
        
class UpdateCalendarList(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        # Get the authorized Http object created by the decorator.
        http = decorator.http()
        
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        mappings = [
                    {"title": "testEvent1",
                     "reflectorList": ["trevor.latson@gmail.com", "zachbwhaley@gmail.com", "neweremailAddress@testEvent1reflectorList.mappings"],
                     "nextStartTime": "now!",
                     "recurringTime": "Every Tuesday at 10:00am",
                     "location": "Trevor's House"},
                    ]
        
        response = calendarListUpdate.updateCalendarList(mappings, calendarId, http)
        self.response.out.write(response)

                
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/calendars.json', GetCalendarList),
    ('/events.json', GetEvents),
    ('/single-events.json', GetSingleEvents),
    ('/update-calendar', UpdateCalendarList),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
