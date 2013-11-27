import json
import webapp2
import calendarListUpdate
import calendarCertificate

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


class GetCertificate(webapp2.RequestHandler):
    def get(self):
        calendarCertificate.getCertificate()
        #print (http)        
        #self.response.out.write(http)

class GetReflectorList(webapp2.RequestHandler):
    def get(self):          
        reflectorList = self.request.get('reflectorList')
        emails = calendarListUpdate.getReflectorList(reflectorList, displayWarning = False) 
        self.response.out.write(json.dumps(emails))
        
class GetCalendarList(webapp2.RequestHandler):
    def get(self):          
        calendarId = self.request.get('calendarId')
        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"
        calendar_list = calendarListUpdate.getReflectorList(calendarId) 
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
        events = calendarListUpdate.getSingleEvents(calendarId, pageToken=None) 
        self.response.out.write(json.dumps(events))
         
class UpdateEvent(webapp2.RequestHandler):
    def get(self):
        event = self.request.get('event')          
        calendarId = self.request.get('calendarId')
        reflectorList = self.request.get('reflectorList')
        status = calendarListUpdate.updateEvent(event, calendarId, reflectorList)
        self.response.out.write(status)

        
class UpdateCalendarList(webapp2.RequestHandler):
    def get(self):
        calendarId = self.request.get('calendarId')
        TimezoneOffset = self.request.get('TimezoneOffset')
        status = calendarListUpdate.updateCalendarList(calendarId, TimezoneOffset, debug = True)
        self.response.out.write(status)

        

                
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/groups', GetGroups),
    ('/certificate', GetCertificate),
    ('/reflectors', GetReflectorList),
    ('/calendars', GetCalendarList),
    ('/events', GetEvents),
    ('/single-events', GetSingleEvents),
    ('/update-event', UpdateEvent),
    ('/update-calendar', UpdateCalendarList)
], debug=True)
