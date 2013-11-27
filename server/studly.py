import json
import webapp2

from google.appengine.ext import ndb

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Studly")

class GetReflectorList(webapp2.RequestHandler):
    def get(self):          
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(["foo", "bar"]))
        
class GetCalendarList(webapp2.RequestHandler):
    def get(self):          
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(["foo", "bar"]))
        
class GetEvents(webapp2.RequestHandler):
    def get(self):          
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(["foo", "bar"]))
        
class GetSingleEvents(webapp2.RequestHandler):
    def get(self):          
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(["foo", "bar"]))
         
class UpdateEvent(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(True))
        
class UpdateCalendarList(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(True))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/reflectors.json', GetReflectorList),
    ('/calendars.json', GetCalendarList),
    ('/events.json', GetEvents),
    ('/single-events.json', GetSingleEvents),
    ('/update-event', UpdateEvent),
    ('/update-calendar', UpdateCalendarList)
], debug=True)
