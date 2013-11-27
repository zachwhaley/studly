import json
import webapp2

from google.appengine.ext import ndb

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Studly")

class GetReflectorList(webapp2.RequestHandler):
    def get(self):          
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(["emailaddress1@foo.com", "emailaddress2@foo.com"]))
        
class GetCalendarList(webapp2.RequestHandler):
    def get(self):          
        self.response.headers['Content-Type'] = 'application/json'
        calendar_list = [{
                          "kind": "calendar#calendarListEntry",
                          "etag": "0MAR7UdiMyUNDlceNGt_2sHPXk4/aOZ-T3e4J4bEfydljdeBBOVF8UU",
                          "id": "trevor.latson@gmail.com",
                          "summary": "trevor.latson@gmail.com",
                          "description": "Your contacts' birthdays and anniversaries",
                          "location": "Austin",
                          "timeZone": "America/Chicago",
                          "summaryOverride": "I've never seen this used...",
                          "colorId": "22",
                          "backgroundColor": "#fa573c",
                          "foregroundColor": "#000000",
                          "hidden": False,
                          "selected": True,
                          "accessRole": "reader",
                          "defaultReminders": [
                            {
                              "method": "email",
                              "minutes": 30
                            }
                          ],
                          "primary": True
                          }, 
                         {
                          "kind": "calendar#calendarListEntry",
                          "etag": "etag string",
                          "id": "string",
                          "summary": "string",
                          "description": "string",
                          "location": "string",
                          "timeZone": "string",
                          "summaryOverride": "string",
                          "colorId": "string",
                          "backgroundColor": "string",
                          "foregroundColor": "string",
                          "hidden": True,
                          "selected": False,
                          "accessRole": "string",
                          "defaultReminders": [
                            {
                              "method": "string",
                              "minutes": 5
                            }
                          ],
                          "primary": False
}]
        self.response.out.write(json.dumps(calendar_list))
        
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
