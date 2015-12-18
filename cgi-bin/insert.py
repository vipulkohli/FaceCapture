#!/usr/bin/env python2.7

import cgi   # NEW
import pymongo, os, json
# ALIASES
getFiles = os.listdir
def main(): # NEW except for the call to processInput
    form = cgi.FieldStorage()      # standard cgi script lines to here!
    db = pymongo.MongoClient().faces.entries
    # face is the database
    # faces is the collection
    records = []
    textfiles = 0
    DATADIRS = ["facedata"]
    for DATADIR in DATADIRS:
                    fileCollection = getFiles( DATADIR );		
                    for filename in fileCollection :
                            filepath = DATADIR + "/" + filename
                            jstr = open( filepath, "r" ).read()
                            textfiles = textfiles + 1	
                            #jstr = jstr[0:-1]
                            pymap = json.loads( jstr )	 
                            db.insert( pymap )
    print "ALL RECORDS INSERTED"

try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    main() 
except:
    cgi.print_exception()                 # catch and print errors
