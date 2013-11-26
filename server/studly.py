import json
import webapp2
import calendarListUpdate

from google.appengine.ext import ndb

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Studly")

class GetGroups(webapp2.RequestHandler):
    def get(self):
        events = [
            {"name": "foo", "joined": True},
            {"name": "bar", "joined": False}
        ]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(events))


class GetReflectorList(webapp2.RequestHandler):
    def get(self):          
        reflectorList = self.request.get('reflectorList')
        emails = calendarListUpdate.getReflectorList(reflectorList, displayWarning = False) 
        self.response.out.write(emails)
        
class GetCalendarList(webapp2.RequestHandler):
    def get(self):          
        calendarId = self.request.get('calendarId')
        calendar_list = calendarListUpdate.getReflectorList(calendarId) 
        self.response.out.write(calendar_list)
        
class GetEvents(webapp2.RequestHandler):
    def get(self):          
        calendarId = self.request.get('calendarId')
        events = calendarListUpdate.getEvents(calendarId, pageToken=None) 
        self.response.out.write(events)
        
class GetSingleEvents(webapp2.RequestHandler):
    def get(self):          
        calendarId = self.request.get('calendarId')
        events = calendarListUpdate.getSingleEvents(calendarId, pageToken=None) 
        self.response.out.write(events)
         
class UpdateEvent(webapp2.RequestHandler):
    def get(self):
        event = self.request.get('event')          
        calendarId = self.request.get('calendarId')
        reflectorList = self.request.get('reflectorList')
        calendarListUpdate.updateEvent(event, calendarId, reflectorList)
        
class UpdateCalendarList(webapp2.RequestHandler):
    def get(self):
        calendarId = self.request.get('calendarId')
        TimezoneOffset = self.request.get('TimezoneOffset')
        calendarListUpdate.updateCalendarList(calendarId, TimezoneOffset, debug = True)
        

                
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/groups', GetGroups),
    ('/reflectors', GetReflectorList),
    ('/calendars', GetCalendarList),
    ('/events', GetEvents),
    ('/single-events', GetSingleEvents),
    ('/update-event', UpdateEvent),
    ('/update-calendar', UpdateCalendarList)
], debug=True)
