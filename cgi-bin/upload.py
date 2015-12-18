#!/usr/bin/env python2.7

import cgi, json, pymongo   # NEW


# reads in text from a web site and returns as string
def http_get_contents( url ):
    import urllib2
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    return res.read()

def insert( pymap ):
	db = pymongo.MongoClient().faces.entries
	db.insert( pymap )

def main():
	form = cgi.FieldStorage()
	firstname = form.getvalue('firstname')
	lastname  = form.getvalue('lastname')
	filename = form.getvalue('filename')
	if( not filename ):
		print "File Name not received"
		return 0
	faceurl = "http://162.249.2.138/uploader/upload/" + filename
	fpp = "https://apius.faceplusplus.com/v2/detection/detect?api_key=4360d1e08dc08a0204802039d1c3bd42&api_secret=h9kpl74mULPIXiW2eNn2ccpyEQAvaFTi&url="
	fpp = fpp + faceurl + "&attribute=age%2Cgender%2Crace%2Csmiling%2Cpose%2Cglass&mode=commercial";
	doc = json.loads( http_get_contents( fpp ) )
	doc["link"] = faceurl
	doc["firstname"] = firstname
	doc["lastname"] = lastname
	doc["category"] = "Uploads"
	wrapper = """
		<script src="http://162.249.2.138/style/voice.js"></script>
		<p> firstname lastname - Face insertfacenum of insertfacetotal </p>
		<ul>
			<li>Smiling: insertemotion</li>
			<li>Goggles: insertlenses</li>
			<li>Gender: insertsex</li>
			<li>Skin: insertskin</li>
			<li>Age: insertage</li>
		</ul>
		<input onclick='responsiveVoice.speak("firstname lastname is a talkskin talksex with age insertage years old");' value="Play Voice" type="button">
	"""
	final = ""
	totalFaces = len(doc['face'])
	if( totalFaces > 0 ):
		insert( doc )
		k = 0
		building = wrapper.replace("firstname", doc['firstname'].title() ).replace("lastname", doc['lastname'].title() )
		building = building.replace("insertfacenum", str( k + 1 ) ).replace("insertfacetotal", str( totalFaces ) )
		building = building.replace( "insertlenses", doc['face'][k]['attribute']['glass']['value'] + " Confidence: " + str( doc['face'][k]['attribute']['glass']['confidence'] ) )
		building = building.replace( "insertsex", doc['face'][k]['attribute']['gender']['value'] + " Confidence: " + str( doc['face'][k]['attribute']['gender']['confidence'] ) )
		building = building.replace( "talksex", doc['face'][k]['attribute']['gender']['value'] )
		building = building.replace( "talkskin", doc['face'][k]['attribute']['race']['value'] )
		building = building.replace( "insertskin", doc['face'][k]['attribute']['race']['value'] + " Confidence: " + str( doc['face'][k]['attribute']['race']['confidence'] ) )
		building = building.replace( "insertage", str( doc['face'][k]['attribute']['age']['value'] ) )
		building = building.replace( "talkskin", doc['face'][k]['attribute']['race']['value'] )
		building = building.replace( "talksex", doc['face'][k]['attribute']['gender']['value'] )
		if doc['face'][k]['attribute']['smiling']['value'] > 60:
			decision = "Yes"
		else:
			decision = "No"
		final = final + building.replace( "insertlink" , doc['link'] ).replace( "insertemotion", decision + " Value: " + str( doc['face'][k]['attribute']['smiling']['value'] ) )
	else:
		final = "No faces detected"
	
	print final

try:   # NEW
	print("Content-type: text/html\n\n")   # say generating html
	print("")
	main()
except:
	cgi.print_exception()                 # catch and print errors
