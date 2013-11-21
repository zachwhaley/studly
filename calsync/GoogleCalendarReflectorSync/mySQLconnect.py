#!/usr/bin/python

import MySQLdb
import pprint

# Open database connection
db = MySQLdb.connect("mp.si2.org","si2server","Ud0ntnoth1s","gforge" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print "MySQL Database version : %s " % data


# Send SQL query to READ a record from the database
def read(debug = False):
    # construct the sql string
    sql = 'select id, seriesTitle, listFile, nextMeeting, regularMeeting from tblCalSerMap '
    results = []
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       if debug:
          pprint.pprint (results)
    except:
        print "End of table"
    return results

# Send SQL query to UPDATE a record with a specified seriesTitle
def updateStartTime(seriesTitle, nextMeeting, debug = False):
    # construct the sql string
    sql = 'update tblCalSerMap set' 
    sql = sql + ' nextMeeting="' + str(nextMeeting) + '" '
    sql = sql + ' where seriesTitle="' + str(seriesTitle) + '"'
    if debug:
        print sql
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()
       print 'Update Failed. Rollback initiated.'

# Send SQL query to UPDATE a record with a specified seriesTitle
def updateRecurringMeeting(seriesTitle, regularMeeting, debug = False):
    # construct the sql string
    sql = 'update tblCalSerMap set'
    sql = sql + ' regularMeeting="' + str(regularMeeting) + '"'
    sql = sql + ' where seriesTitle="' + str(seriesTitle) + '"'
    if debug:
        print sql
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()
       print 'Update Failed. Rollback initiated.'

def closeDB():
    db.close()

if __name__ == '__main__':
    # Test calls to read() and update() for debugging purposes
    read(debug = True)
    closeDB()
    #update("TestEvent1",  "test-event1", "NextMeeting1", "RegularMeeting1")
    #update("TestEvent2" , "test-event2")
