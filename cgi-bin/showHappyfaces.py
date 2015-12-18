#!/usr/bin/env python2.7

import cgi   # NEW
import pymongo

db = pymongo.MongoClient().faces.entries

def main():
    print "<table>"    
    for doc in db.find():
        if doc['face'][0]['attribute']['smiling']['value'] > 60:
             print "<tr><td>"
             print "<img width='100' src='" + doc['link'] + "' /></td><td>"
             print doc['firstname']+' '+doc['lastname']+' looks happy.'
             print "</td></tr>"
    print "</table>"
    return True

try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    print("")
    print("""
<!DOCTYPE HTML>
<html>
<head>
	<style>
	img{
		width: 100%;
		border: 3px dashed red;
	}
	td{
		width: 300px;
	}
	</style>
<body>
""")
    main()
    print("</body>")
    print("</html>")
except:
    cgi.print_exception()                 # catch and print errors
