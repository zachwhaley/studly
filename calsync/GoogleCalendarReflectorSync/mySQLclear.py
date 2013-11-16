#!/usr/bin/python

import MySQLdb
import pprint
import mySQLconnect

# Open database connection
db = MySQLdb.connect("mp.si2.org","si2server","Ud0ntnoth1s","gforge" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

def clear(debug = False):
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

    for row in results:
        id = row[0]
        seriesTitle = row[1]
        listFile = row[2]
        nextMeeting = row[3]
        regularMeeting = row[4]
        mySQLconnect.updateStartTime(seriesTitle, "")
        mySQLconnect.updateRecurringMeeting(seriesTitle, "")        

def closeDB():
    db.close()

if __name__ == '__main__':
    # Test calls to read() and update() for debugging purposes
    clear(debug = True)
    closeDB()
