#!/usr/bin/env python2.7

import cgi   # NEW
import pymongo

def main(): # NEW except for the call to processInput
    form = cgi.FieldStorage()      # standard cgi script lines to here!
    db = pymongo.MongoClient().faces.entries
    entry = db.find_one()
    print( "<img src='" + entry['link'] + "' />" )

try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    main() 
except:
    cgi.print_exception()                 # catch and print errors
