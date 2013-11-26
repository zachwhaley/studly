#!/usr/bin/python

import sys
import pprint
import time
import datetime
import calendarAuthenticate
#import mySQLconnect
from dateutil import parser

def getReflectorList(reflectorList, displayWarning = False):
#     reflectorList = "/var/lib/majordomo/lists/" + reflectorList
#     try: 
#         refList = open(reflectorList , 'r' )
#     except:
#       if displayWarning == True:
#         print "WARNING: Reflector List not found: " + reflectorList
#         exit(1)
#     emails = []
#     while True:
#         oneLine = refList.readline()
#         if not oneLine:
#             break
#         if len(oneLine) > 4:
#             emails.append(str.strip(oneLine.lower()))
    emails = ["trevor.latson@gmail.com", "zachbwhaley@gmail.com"]
    return emails

def getCalendarList(calendarId):
    page_token = None
    while True:
        service = calendarAuthenticate.getService(calendarId)
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    
    return calendar_list


def getEvents(calendarId, pageToken=None):
    # set up a time interval from t-24hrs to t+365 days
    yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
    nextYear =  datetime.datetime.now() + datetime.timedelta(days=365)
    # get events list from google using RFC 3339 timestamps with -00:00 timezone offset
    service = calendarAuthenticate.getService(calendarId)
    events = service.events().list(
        calendarId=calendarId,
        singleEvents=False,
        #maxResults=1000,
        timeMin=yesterday.isoformat('T') + "-00:00",
        timeMax=nextYear.isoformat('T') + "-00:00",
        timeZone="America/Chicago",
        #pageToken=pageToken
        #q= "custom search string goes here..."
        ).execute()
    return events


def getSingleEvents(calendarId, pageToken=None):
    # set up a time interval from t=0 to t+365 days
    nextYear =  datetime.datetime.now() + datetime.timedelta(days=365)
    # get single event list from google using RFC 3339 timestamps with -00:00 timezone offset
    service = calendarAuthenticate.getService(calendarId)
    events = service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        orderBy="startTime",
        #maxResults=1000,
        timeMin=datetime.datetime.now().isoformat('T') + "-00:00",
        timeMax=nextYear.isoformat('T') + "-00:00",
        timeZone="America/Chicago",
        #pageToken=pageToken
        #q= "custom search string goes here..."
        ).execute()
    return events


def updateEvent(event, calendarId, reflectorList, debug = False):
    reflectorEmails = getReflectorList(reflectorList, displayWarning = True)
    eventEmails = []
    attendeeRemovals = []
    addedEmails = []
    exceptionList = []
    try:
        exceptionList = getReflectorList(reflectorList + ".exp")
        print "Exception List Found"
    except:
        pass
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
            if emailf not in reflectorEmails or emailf in exceptionList:
                print 'Removing: ' , attendee['email'] , 'from the event: ' , event['summary'], 'occuring on: ', event['start']['dateTime']
                attendeeRemovals.append(attendee)
                update = True
                numUpdates = numUpdates + 1

    for attendeeRemoval in attendeeRemovals:
            event['attendees'].remove(attendeeRemoval)
    
    for oneReflectorEmail in reflectorEmails:
        if numUpdates < 3:
            # add attendees if ther email address IS on the reflector list but not on the attendee list
            if oneReflectorEmail not in eventEmails and oneReflectorEmail not in exceptionList:
                print 'Adding: ' , oneReflectorEmail , 'to the event: ' , event['summary'], 'occuring on: ', event['start']['dateTime']
                event['attendees'].append( dict( email = oneReflectorEmail, responseStatus = 'needsAction' ) )
                update = True
                numUpdates = numUpdates + 1

    if update: 
        if debug == False:
            #raw_input("Press Enter to commit changes...")
            service = calendarAuthenticate.getService(calendarId)
            try:
                service.events().update(calendarId=calendarId, eventId=event['id'], body=event, sendNotifications = True).execute()
            except: 
                print "WARNING: Calendar Usage Limits Exceeded."
            time.sleep(10)


def updateCalendarList(calendarId, TimezoneOffset, debug = True):
    print "The current time is: " , datetime.datetime.now()
    eventsRead = []
    # Set a condition code for update failure (ie calendar usage limits exceed)
    updateFail = False
    # Retrieve the list of calendars and remove the holiday and birthdays calendars from the list 
    calendar_list = getCalendarList(calendarId)
    # Read the MySQL database that maps event titles to reflector list filenames
    #mySQLdb = mySQLconnect.read()
    mySQLdb = []
    # Iterate through all calendars
    for calendar in calendar_list['items']:
      if calendar['id'] == calendarId:
        print "Searching events in calendar: " + calendar['id']
        # Get events from this calendar. Returns the parent recurrence for recurring events, and not individual instances
        events = getEvents(calendarId)
        # Get single events from this calendar. Returns the individual instances of recurring events ordered by start date
        nextEvents = getSingleEvents(calendarId)
        
        for event in events['items']:
                # Iterate through rows from the MySQL database and assign titles to rows
                for row in mySQLdb:
                    id = row[0]
                    seriesTitle = row[1]
                    listFile = row[2]
                    nextMeeting = row[3]
                    regularMeeting = row[4]
                    # If the event title is found in the MySQL database, output event info, 
                    # then call updateEvent with event name and reflectorList name
                    if 'summary' in event:
                        if event['summary'] == seriesTitle:
                           if event['organizer']['email'] == calendar['id']:
                               #mySQLconnect.updateStartTime(seriesTitle, "")
                               #mySQLconnect.updateRecurringMeeting(seriesTitle, "")
                               print "\nExamining the event: " , event['summary']
                               # Output recurring event information and update the MySQL database
                               if 'recurrence' in event:
                                   #mySQLconnect.updateRecurringMeeting(seriesTitle, "")
                                   print "The event recurs: "
                                   originalStartTime = datetime.datetime.strptime( str( event['start']['dateTime'] )[0:19], '%Y-%m-%dT%H:%M:%S' )
                                   
                                   # Correct for Timezone offsets
                                   originalStartTime = originalStartTime + datetime.timedelta(hours = TimezoneOffset)
                                   
                                   # Parse the RRULE into a dictionary
                                   RRULE = str(event['recurrence'][0])
                                   rrulef = RRULE.split(';')
                                   rruleDict = {}                                    
                                   for section in rrulef:
                                       keyValuePair = section.split('=')
                                       rruleDict[ keyValuePair[0] ] = keyValuePair[1]

                                   # Display information for weekly recurring events and update the mySQL database
                                   ordinals = {'1': 'first', '2': 'second', '3': 'third', '4': 'forth', '-': 'last'}
                                   if rruleDict['RRULE:FREQ'] == 'WEEKLY':
                                       if 'INTERVAL' not in rruleDict:
                                           regularStartTimef = "Weekly on %s at %s" % ( originalStartTime.strftime("%A"), originalStartTime.strftime("%I:%M%p") )
                                           #mySQLconnect.updateRecurringMeeting(seriesTitle, regularStartTimef)
                                           print regularStartTimef
                                       else:
                                           regularStartTimef = "Every " + rruleDict['INTERVAL'] + " weeks on %s at %s" % ( originalStartTime.strftime("%A"), originalStartTime.strftime("%I:%M%p") )
                                           #mySQLconnect.updateRecurringMeeting(seriesTitle, regularStartTimef)
                                           print regularStartTimef
                                   
                                   # Display information for monthly recurring events and update the mySQL database
                                   if rruleDict['RRULE:FREQ'] == 'MONTHLY':
                                      if len(rruleDict['BYDAY']) > 2:
                                          regularStartTimef = "Monthly on the %s %s at %s" % (ordinals[ rruleDict['BYDAY'][0:1] ], originalStartTime.strftime("%A"), originalStartTime.strftime("%I:%M%p") )
                                          #mySQLconnect.updateRecurringMeeting(seriesTitle, regularStartTimef)
                                          print regularStartTimef
                                      else:
                                          regularStartTimef = "Monthly on day %s at %s" % (originalStartTime.strftime("%d"), originalStartTime.strftime("%I:%M%p") )
                                          #mySQLconnect.updateRecurringMeeting(seriesTitle, regularStartTimef)
                                          print regularStartTimef

                                    
                               # Output single event information and update the MySQL database
                               if 'start' in event:
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
                                                               #mySQLconnect.updateStartTime(seriesTitle, nextStartTimef)
                                                               eventsRead.append(nextEvent['summary'])
                                                               break
                               else:
                                   print "No Start Date Found!"
                                  
                               try:
                                   updateEvent( event, calendarId, listFile, debug )
                               except KeyboardInterrupt:
                                   print 'Update canceled. Moving to next event.'

        
if __name__ == '__main__':


    if len(sys.argv) > 2:
        calendarId = sys.argv[1]
        TimezoneOffset = sys.argv[2]
        updateCalendarList(calendarId, int(TimezoneOffset), debug = False)
        #mySQLconnect.closeDB()

    else:
        print "Error: calendarId and/or timezone offset command line argument not specified. Format is ./calendarListUpdate.py <calendarId> <TimezoneOffset> "
        exit(1)

