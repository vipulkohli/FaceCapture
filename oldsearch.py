#!/usr/bin/env python2.7

import cgi   # NEW
import pymongo

db = pymongo.MongoClient().faces.entries
id_list=[]

def init(): # NEW except for the call to processInput
    form = cgi.FieldStorage()      # standard cgi script lines to here!
    db = pymongo.MongoClient().faces.entries
    #firstname=raw_input("please input first name:")
    #lastname=raw_input("please input last name:")

    firstname="drake"
    lastname="bell"

    for doc in db.find({'lastname':lastname,'firstname':firstname}):
        id_list.append(doc['_id'])
    return id_list

def main():
    my_id=init()
    if len(my_id)==0:
       print "no matched pictures."
    else:
       print str(len(my_id))+" matched pictures."
       print '--------------------------------------------'
       print "<table>"
       for pic in my_id:
           for doc in db.find({'_id':pic}):
               print "<tr><td>"
               if doc['face'][0]['attribute']['smiling']['value'] > 60:
                   print "<img width='100' src='" + doc['link'] + "' /></td><td>"
                   print doc['firstname']+' '+doc['lastname']+' looks happy.'               
               else:
                   print "<img src='" + doc['link'] + "' /></td><td>"
                   print doc['firstname']+' '+doc['lastname']+' looks not happy.'
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
