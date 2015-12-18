#!/usr/local/bin/python2.7

import cgitb
import cgi
import urllib
import json

parms = cgi.FieldStorage()
print "Content-type: application/json\n\n"

EXIT_SUCCESS = 'true'
EXIT_FAILURE = 'false'

def isJsonString( inString ):
    try :
        # loads safely parses strings with
        # brackets, spaces, quotes,
        # WARNING: treats primitive data types
        # as valid JSON, although these are not
        # literal respresentations of JS objects
        json.loads( inString )
        return EXIT_SUCCESS
    except ValueError :
        return EXIT_FAILURE

if len(parms) == 0 :
	print EXIT_FAILURE

elif len(parms) == 1 : 
	for k in parms.keys() :
		target = str( urllib.unquote( parms[k].value ).decode('utf8') )
		print isJsonString( target )

else: # 2+ HTTP parmaters find param "json"
	found = EXIT_FAILURE;
	for k in parms.keys() :
		if k == "json" :
			target = str( urllib.unquote( parms[k].value ).decode('utf8') )
			found = isJsonString( target )
	print found