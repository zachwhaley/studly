import json
import webapp2
import calendarListUpdate
import os

from google.appengine.ext import ndb
from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

decorator = OAuth2DecoratorFromClientSecrets(
  os.path.join(os.path.dirname(__file__), 'client_secret_656176414432.apps.googleusercontent.com.json'),
  scope='https://www.googleapis.com/auth/calendar')

service = build('calendar', 'v3')


class Mapping(ndb.Model):
    title = ndb.StringProperty()
    htmlLink = ndb.StringProperty()
    reflectorList = ndb.StringProperty(repeated=True)
    calendarId = ndb.StringProperty()
    nextStartTime = ndb.StringProperty()
    recurringStartTime = ndb.StringProperty()
    location = ndb.StringProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()


class AddEmail(webapp2.RequestHandler):
    def get(self):
        self.redirect('/myevents')
    @decorator.oauth_required
    def post(self):
        # Get the authorized Http object created by the decorator.
        http = decorator.http()

        # Retrieve the mapping with the title specified
        mapping = Mapping.query(Mapping.title == self.request.get('title')).fetch()[0]
        # Append the specified emailAddress to the mapping object
        mapping.reflectorList.append(self.request.get('emailAddress'))
        # Call UpdateCalendarList with the updated mapping object
        mapping = calendarListUpdate.updateCalendarList(mapping, self.request.get('calendarId'), http)
        # And store the updated mapping object in the datastore
        mapping.put()
        self.redirect('/myevents')


class RemoveEmail(webapp2.RequestHandler):
    def get(self):
        self.redirect('/myevents')
    @decorator.oauth_required
    def post(self):
        # Get the authorized Http object created by the decorator.
        http = decorator.http()

        # Retrieve the mapping with the title specified
        mapping = Mapping.query(Mapping.title == self.request.get('title')).fetch()[0]
        # Append the specified emailAddress to the mapping object
        mapping.reflectorList.remove(self.request.get('emailAddress'))
        # Call UpdateCalendarList with the updated mapping object
        mapping = calendarListUpdate.updateCalendarList(mapping, self.request.get('calendarId'), http)
        # And store the updated mapping object in the datastore
        mapping.put()
        self.redirect('/myevents')


class GetMappings(webapp2.RequestHandler):
    def get(self):
        # Sweet one-liner.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps([m.to_dict() for m in Mapping.query().fetch()]))
        
                   
class GetCalendarList(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        # Get the authorized Http object created by the decorator.
        http = decorator.http()

        #hard-coded data for testing purposes:
        calendarId = "trevor.latson@gmail.com"

        calendar_list = calendarListUpdate.getCalendarList(calendarId, http)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(calendar_list))


class ImportEvent(webapp2.RequestHandler):
    def get(self):
        self.redirect('/myevents')
    @decorator.oauth_required
    def post(self):
        # Get the authorized Http object created by the decorator.
        http = decorator.http()
        mapping = Mapping()
        mapping.title = self.request.get('title')
        mapping.calendarId = self.request.get('calendarId')
        mapping = calendarListUpdate.updateCalendarList(mapping, mapping.calendarId, http)
        mapping.put()
        self.redirect('/myevents')


class JoinEvent(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')
    @decorator.oauth_required
    def post(self):
        # Get the authorized Http object created by the decorator.
        http = decorator.http()

        # Retrieve the mapping with the title specified
        mapping = Mapping.query(Mapping.title == self.request.get('title')).fetch()[0]
        # Append the specified emailAddress to the mapping object
        mapping.reflectorList.append(self.request.get('emailAddress'))
        # Call UpdateCalendarList with the updated mapping object
        mapping = calendarListUpdate.updateCalendarList(mapping, self.request.get('calendarId'), http)
        # Store the updated mapping object in the datastore
        mapping.put()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(mapping.to_dict()))
        self.redirect('/')


class RemoveEvent(webapp2.RequestHandler):
    def get(self):
        self.redirect('/myevents')
    def post(self):
        # Retrieve the mapping with the title specified
        mappings = Mapping.query(Mapping.title == self.request.get('title')).fetch()
        # Iterate through each mapping object that matches the specified event title (usually just one)
        for mapping in mappings:
            # Remove the mapping from the datastore
            mapping.key.delete()
        self.redirect('/myevents')


app = webapp2.WSGIApplication([
    ('/get-mappings.json', GetMappings),
    ('/add-email', AddEmail),
    ('/remove-email', RemoveEmail),
    ('/import-event', ImportEvent),
    ('/join-event', JoinEvent),
    ('/remove-event', RemoveEvent),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
