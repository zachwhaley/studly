import json
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Studly")

class GetMappings(webapp2.RequestHandler):
    def get(self):
        mappings = [{"title": "testEvent1",
                     "reflectorList": ["trevor.latson@gmail.com", "zachbwhaley@gmail.com"],
                     "nextStartTime": "now!",
                     "recurringTime": "Every Tuesday at 10:00am",
                     "location": "Trevor's House"},
                    {"title": "testEvent1",
                     "reflectorList": ["trevor.latson@gmail.com", "zachbwhaley@gmail.com"],
                     "nextStartTime": "now!",
                     "recurringTime": "Every Tuesday at 10:00am",
                     "location": "Trevor's House"},
        ]
        self.response.out.write(json.dumps(mappings))

class EventManager(webapp2.RequestHandler):
    def post(self):
        self.redirect('/groups')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/mappings.json', GetMappings),
    ('/join', EventManager),
    ('/leave', EventManager),
], debug=True)
