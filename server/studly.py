import json
import webapp2
import datetime

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
        events = [{
                  "kind": "calendar#event",
                  "etag": "etag",
                  "id": "string",
                  "status": "string",
                  "htmlLink": "string",
                  "created": datetime,
                  "updated": datetime,
                  "summary": "string",
                  "description": "string",
                  "location": "string",
                  "colorId": "string",
                  "creator": {
                    "id": "string",
                    "email": "string",
                    "displayName": "string",
                    "self": True
                  },
                  "organizer": {
                    "id": "string",
                    "email": "string",
                    "displayName": "string",
                    "self": True
                  },
                  "start": {
                    "date": datetime.date,
                    "dateTime": datetime,
                    "timeZone": "string"
                  },
                  "end": {
                    "date": datetime.date,
                    "dateTime": datetime,
                    "timeZone": "string"
                  },
                  "endTimeUnspecified": True,
                  "recurrence": [
                    "string"
                  ],
                  "recurringEventId": "string",
                  "originalStartTime": {
                    "date": datetime.date,
                    "dateTime": datetime,
                    "timeZone": "string"
                  },
                  "transparency": "string",
                  "visibility": "string",
                  "iCalUID": "string",
                  "sequence": 2,
                  "attendees": [
                    {
                      "id": "string",
                      "email": "string",
                      "displayName": "string",
                      "organizer": True,
                      "self": True,
                      "resource": True,
                      "optional": True,
                      "responseStatus": "string",
                      "comment": "string",
                      "additionalGuests": 2
                    }
                  ],
                  "attendeesOmitted": True,
                  "extendedProperties": {
                    "private": {
                      "(key)": "string"
                    },
                    "shared": {
                      "(key)": "string"
                    }
                  },
                  "hangoutLink": "string",
                  "gadget": {
                    "type": "string",
                    "title": "string",
                    "link": "string",
                    "iconLink": "string",
                    "width": 2,
                    "height": 2,
                    "display": "string",
                    "preferences": {
                      "(key)": "string"
                    }
                  },
                  "anyoneCanAddSelf": True,
                  "guestsCanInviteOthers": True,
                  "guestsCanModify": True,
                  "guestsCanSeeOtherGuests": True,
                  "privateCopy": True,
                  "locked": True,
                  "reminders": {
                    "useDefault": True,
                    "overrides": [
                      {
                        "method": "string",
                        "minutes": 2
                      }
                    ]
                  },
                  "source": {
                    "url": "string",
                    "title": "string"
                  }
                }]
        self.response.out.write(json.dumps(events))
        
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
