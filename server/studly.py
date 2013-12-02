import json
import webapp2

class GetMappings(webapp2.RequestHandler):
    def get(self):
        mappings = [{"title": "testEvent1",
                     "reflectorList": ["trevor.latson@gmail.com", "zachbwhaley@gmail.com"],
                     "nextStartTime": "now!",
                     "recurringTime": "Every Tuesday at 10:00am",
                     "location": "Trevor's House"},
                    {"title": "testEvent2",
                     "reflectorList": ["trevor.latson@gmail.com", "zachbwhaley@gmail.com"],
                     "nextStartTime": "now!",
                     "recurringTime": "Every Tuesday at 10:00am",
                     "location": "Trevor's House"},
        ]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(mappings))

class EventManager(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email')
        self.response.out.write(email)
        event = self.request.get('event')
        self.response.out.write(event)

app = webapp2.WSGIApplication([
    ('/mappings.json', GetMappings),
    ('/join', EventManager),
    ('/leave', EventManager),
], debug=True)
