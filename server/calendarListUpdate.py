#!/usr/bin/python

import sys
import pprint
import time
import datetime

from dateutil import parser

from google.appengine.ext import ndb
from apiclient.discovery import build
from google.appengine.ext import webapp

service = build('calendar', 'v3')


def getCalendarList(httpAuth):
    request = service.calendarList().list()
    response = request.execute(http=httpAuth)
    return response

def getSettings(httpAuth):
    request = service.settings().list()
    response = request.execute(http=httpAuth)
    return response


def getEvents(calendarId, httpAuth):
    # set up a time interval from t-24hrs to t+365 days
    yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
    nextYear =  datetime.datetime.now() + datetime.timedelta(days=365)
    # get events list from google using RFC 3339 timestamps with -00:00 timezone offset
    request = service.events().list(
        calendarId=calendarId,
        singleEvents=False,
        #maxResults=1000,
        timeMin=yesterday.isoformat('T') + "-00:00",
        timeMax=nextYear.isoformat('T') + "-00:00",
        timeZone="America/Chicago",
        #q= "custom search string goes here..."
        )
    response = request.execute(http=httpAuth)
    return response


def getSingleEvents(calendarId, httpAuth):
    # set up a time interval from t=0 to t+365 days
    nextYear =  datetime.datetime.now() + datetime.timedelta(days=365)
    # get single event list from google using RFC 3339 timestamps with -00:00 timezone offset
    request = service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        orderBy="startTime",
        #maxResults=1000,
        timeMin=datetime.datetime.now().isoformat('T') + "-00:00",
        timeMax=nextYear.isoformat('T') + "-00:00",
        timeZone="America/Chicago",
        #q= "custom search string goes here..."
        )
    response = request.execute(http=httpAuth)
    return response

def parseRecurrenceRule(event, entry, TimezoneOffset = 0):
    print "The event recurs: "
    originalRecurringTime = datetime.datetime.strptime( str( event['start']['dateTime'] )[0:19], '%Y-%m-%dT%H:%M:%S' )
   
    # Correct for Timezone offsets
    originalRecurringTime = originalRecurringTime + datetime.timedelta(hours = TimezoneOffset)
   
    # Parse the RRULE (recurrence rule) into a dictionary
    RRULE = str(event['recurrence'][0])
    rrulef = RRULE.split(';')
    rruleDict = {}                                    
    for section in rrulef:
        keyValuePair = section.split('=')
        rruleDict[ keyValuePair[0] ] = keyValuePair[1]

    # Display information for weekly recurring events and update the mappings object
    ordinals = {'1': 'first', '2': 'second', '3': 'third', '4': 'forth', '-': 'last'}
    if rruleDict['RRULE:FREQ'] == 'WEEKLY':
        if 'INTERVAL' not in rruleDict:
            #update the mappings with the weekly event starting time, and print it to the console
            recurringStartTimef = "Weekly on %s at %s" % ( originalRecurringTime.strftime("%A"), originalRecurringTime.strftime("%I:%M%p") )
            entry['recurringTime'] = recurringStartTimef
            print recurringStartTimef
            return entry
        else:
            #update the mappings with the semi-weekly event starting time, and print it to the console
            recurringStartTimef = "Every " + rruleDict['INTERVAL'] + " weeks on %s at %s" % ( originalRecurringTime.strftime("%A"), originalRecurringTime.strftime("%I:%M%p") )
            entry['recurringTime'] = recurringStartTimef
            print recurringStartTimef
            return entry
   
    # Display information for monthly recurring events and update the mappings object
    if rruleDict['RRULE:FREQ'] == 'MONTHLY':
       if len(rruleDict['BYDAY']) > 2:
           #update the mappings with the monthly event starting time, and print it to the console
           recurringStartTimef = "Monthly on the %s %s at %s" % (ordinals[ rruleDict['BYDAY'][0:1] ], originalStartTime.strftime("%A"), originalStartTime.strftime("%I:%M%p") )
           entry['recurringTime'] = recurringStartTimef
           print recurringStartTimef
           return entry
       else:
           #update the mappings with the monthly (by day) event starting time, and print it to the console
           recurringStartTimef = "Monthly on day %s at %s" % (originalStartTime.strftime("%d"), originalStartTime.strftime("%I:%M%p") )
           entry['recurringTime'] = recurringStartTimef
           print recurringStartTimef
           return entry

def parseSingleRule(nextEvents, event, entry, TimezoneOffset = 0):
    eventsRead = []
    for nextEvent in nextEvents['items']:
        if 'summary' in nextEvent:
            if nextEvent['summary'] == event['summary']:
                if 'start' in nextEvent:
                    if 'dateTime' in nextEvent['start']:
                        nextStartTime = datetime.datetime.strptime( str( nextEvent['start']['dateTime'] )[0:19], '%Y-%m-%dT%H:%M:%S' )
                        # Correct for Timezone offsets
                        nextStartTime = nextStartTime + datetime.timedelta(hours = TimezoneOffset)
                        if nextStartTime > datetime.datetime.now():
                            if nextEvent['summary'] not in eventsRead:
                                nextStartTimef = nextStartTime.strftime("%A, %B %d, %Y %I:%M%p")
                                print "The the next event start time is: \n", nextStartTimef
                                #update the mappings with the next event starting time, and print it to the console
                                entry['nextStartTime'] = nextStartTimef
                                eventsRead.append(nextEvent['summary'])
                                break
    return entry

def updateEvent(event, calendarId, reflectorList, httpAuth, debug = False):
    eventEmails = []
    attendeeRemovals = []
    addedEmails = []

    # Initialize a condition code for event changes
    update = False
    # Initialize a counter for modificaitons to event
    numUpdates = 0

    if 'attendees' not in event:
        event['attendees'] = []
    print "Checking attendee list of event: ",  event['summary']
    for attendee in event['attendees']:
        if numUpdates < 3:
            eventEmails.append(str(attendee['email'].lower()))
            # remove attendees if their email address IS NOT on the reflector list
            emailf = str.strip(str(attendee['email'].lower()))
            if emailf not in reflectorList:
                print 'Removing: ' , attendee['email'] , 'from the event: ' , event['summary'], 'occuring on: ', event['start']['dateTime']
                attendeeRemovals.append(attendee)
                update = True
                #this counter limits the number of modificaitons that are made to a calendar per cycle. For now it is unnecessary. 
                #numUpdates = numUpdates + 1

    for attendeeRemoval in attendeeRemovals:
            event['attendees'].remove(attendeeRemoval)
    
    for oneReflectorEmail in reflectorList:
        if numUpdates < 3:
            # add attendees if ther email address IS on the reflector list but not on the attendee list
            if oneReflectorEmail not in eventEmails:
                print 'Adding: ' , oneReflectorEmail , 'to the event: ' , event['summary'], 'occuring on: ', event['start']['dateTime']
                event['attendees'].append( dict( email = oneReflectorEmail, responseStatus = 'needsAction' ) )
                update = True
                #this counter limits the number of modificaitons that are made to a calendar per cycle. For now it is unnecessary. 
                #numUpdates = numUpdates + 1

    if update: 
        if debug == False:
            try:
                request = service.events().update(calendarId=calendarId, eventId=event['id'], body=event, sendNotifications = True)
                response = request.execute(http=httpAuth)
            except: 
                print "WARNING: Update Unsuccessful. Returning request"
                return request
            return response



def updateCalendarList(mappings, calendarId, httpAuth, TimezoneOffset = 0, debug = False):
    print "The current time is: " , datetime.datetime.now()
    # Set a condition code for update failure (ie calendar usage limits exceed)
    updateFail = False
    # Retrieve the list of calendars
    calendar_list = getCalendarList(httpAuth)

    # Iterate through all calendars
    for calendar in calendar_list['items']:
      if calendar['id'] == calendarId:
        print "Searching events in calendar: " + calendar['id']
        # Get events from this calendar. Returns single entries for recurring events, and not individual instances
        events = getEvents(calendarId, httpAuth)

        
        for event in events['items']:
            # Iterate through each entry in the mappings
            for entry in mappings:
                # If the event title is found in the mappings, output event info to the console, 
                # then call updateEvent with event name and reflectorList
                if 'summary' in event:
                    if event['summary'] == entry['title']:
                       if event['organizer']['email'] == calendar['id']:
                           print "\nExamining the event: " , event['summary']
                           # Make the event public
                           event['visibility'] = "public"
                           # Store the event location to the mappings object
                           entry['location'] = event['location']
                           # Display information for recurring event information to the console and store it to the mappings object
                           if 'recurrence' in event:
                               entry = parseRecurrenceRule(event, entry)                                
                           # Display information for single events to the console and update the mappings object
                           if 'start' in event:
                               # Get single events from this calendar. Returns the individual instances of recurring events ordered by start date
                               nextEvents = getSingleEvents(calendarId, httpAuth)
                               entry = parseSingleRule(nextEvents, event, entry)
                           try:
                               response = updateEvent( event, calendarId, entry['reflectorList'], httpAuth, debug )
                               #print response
                           except KeyboardInterrupt:
                               print 'Update canceled. Moving to next event.'
                               return mappings
                           return mappings