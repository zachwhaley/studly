import json
import webapp2

from google.appengine.ext import ndb

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Studly")

class GetGroups(webapp2.RequestHandler):
    def get(self):
        events = [
            {"name": "foo", "joined": "true"},
            {"name": "bar", "joined": "false"}
        ]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(events))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/groups', GetGroups),
], debug=True)
