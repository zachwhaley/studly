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
        with open('view/reflectors.html', 'r') as f:
            html = f.read()
        self.response.out.write(html)
         
    def post(self):
        fileName = self.request.get('file')  
        self.response.out.write(fileName)
                

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/groups', GetGroups),
    ('/reflectors', GetReflectorList),
], debug=True)
