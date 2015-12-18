#!/usr/bin/env python2.7

import cgi   # NEW
import pymongo

db = pymongo.MongoClient().faces.entries

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

firstname = form.getvalue('firstname')
lastname  = form.getvalue('lastname')
category = form.getvalue('category')

glasses  = form.getvalue('glasses')
skin  = form.getvalue('skin')
smiling = form.getvalue('smiling')
gender = form.getvalue('gender')

target = {}
if( firstname and lastname ):
	target = {"firstname":firstname, "lastname" : lastname}
else:
	firstname = ""
	lastname = ""

if( category ):
	target = { "category" : category }
else:
	category = ""

if( glasses or skin or gender or smiling ):
	elemMatch = { "$elemMatch" : {}  }
	if( smiling == "Yes" ):
		elemMatch["$elemMatch"]["attribute.smiling.value"] = {"$gt" : 60 }
	if( smiling == "No" ):
		elemMatch["$elemMatch"]["attribute.smiling.value"] = {"$lte" : 60 }
	if( glasses ):
		elemMatch["$elemMatch"]["attribute.glass.value"] = glasses
	if( skin ):
		elemMatch["$elemMatch"]["attribute.race.value"] = skin
	if( gender ):
		elemMatch["$elemMatch"]["attribute.gender.value"] = gender
	target["face"] = elemMatch

dataset = db.find( target ).limit(50)

def getCelebList():
	names = ["drake bell", "ashley tisdale", "enrique iglesias", "beyonce knowles", "ariana grande", "sam smith", "bee gees", "bob marley", "adam sandler"]
	names.sort()
	menulist = ""
	menuitem = """<tr><td class="menucell"><a href="?firstname=insertfirstname&lastname=insertlastname" class="menulink">insertcapfirstname insertcaplastname</a></td></tr>"""
	for name in names:
		fullname = name.split()
		firstname = fullname[0]
		lastname = fullname[1]
		appendix = menuitem.replace("insertfirstname", firstname).replace("insertlastname", lastname)
		appendix = appendix.replace("insertcapfirstname", firstname.title() ).replace("insertcaplastname", lastname.title() )
		menulist = menulist + appendix
	return menulist


def bubbleSort( badList, lenses = "", race = "", sex = "", smile = ""  ):
	length = len(badList) - 1
	sorted = False  # We haven't started sorting yet
	if( smile ):
		while not sorted:
		    sorted = True  # Assume the list is now sorted
		    for element in range(0, length):
		        if badList[element]['face'][0]['attribute']['smiling']['value'] < badList[element + 1]['face'][0]['attribute']['smiling']['value']:
		            sorted = False  # We found two elements in the wrong order
		            hold = badList[element + 1]
		            badList[element + 1] = badList[element]
		            badList[element] = hold
	if( lenses ):
		while not sorted:
		    sorted = True  # Assume the list is now sorted
		    for element in range(0, length):
		        if badList[element]['face'][0]['attribute']['glass']['confidence'] < badList[element + 1]['face'][0]['attribute']['glass']['confidence']:
		            sorted = False  # We found two elements in the wrong order
		            hold = badList[element + 1]
		            badList[element + 1] = badList[element]
		            badList[element] = hold
	if( race ):
		while not sorted:
		    sorted = True  # Assume the list is now sorted
		    for element in range(0, length):
		        if badList[element]['face'][0]['attribute']['race']['confidence'] < badList[element + 1]['face'][0]['attribute']['race']['confidence']:
		            sorted = False  # We found two elements in the wrong order
		            hold = badList[element + 1]
		            badList[element + 1] = badList[element]
		            badList[element] = hold
	if( sex ):
		while not sorted:
		    sorted = True  # Assume the list is now sorted
		    for element in range(0, length):
		        if badList[element]['face'][0]['attribute']['gender']['confidence'] < badList[element + 1]['face'][0]['attribute']['gender']['confidence']:
		            sorted = False  # We found two elements in the wrong order
		            hold = badList[element + 1]
		            badList[element + 1] = badList[element]
		            badList[element] = hold
    # We went through the whole list. At this point, if there were no elements
    # in the wrong order, sorted is still True. Otherwise, it's false, and the
    # while loop executes again.
	return badList

def main():
	wrapper = """ 
	<tr class="gridcell">

		<td> <img class="photograph" src="insertlink" />	 </td>

		<td class="photoinfo" >
		
		firstname lastname - insertfacenum of insertfacetotal
		<ul>
			<li>Smiling: insertemotion</li>
			<li>Goggles: insertlenses</li>
			<li>Gender: insertsex</li>
			<li>Skin: insertskin</li>
			<li>Age: insertage</li>
		</ul>

		<input onclick='responsiveVoice.speak("firstname lastname is a talkskin talksex with age insertage years old");' value="Play Voice" type="button">

		</td>

	</tr>
    """    
	final = ""
	collection = []
	for doc in dataset:
		collection.append( doc )
	collection = bubbleSort( collection, lenses = glasses, race = skin, sex = gender, smile = smiling )
	for doc in collection:
		totalFaces = len(doc['face'])
		for k in range( 0, totalFaces ):
			if( not firstname and not category ):
				if( k > 0 ):
					continue
			if( glasses and doc['face'][k]['attribute']['glass']['value'] != glasses ):
				continue
			if( skin and doc['face'][k]['attribute']['race']['value'] != skin ):
				continue
			if( gender and doc['face'][k]['attribute']['gender']['value'] != gender ):
				continue
			building = wrapper.replace("firstname", doc['firstname'].title() ).replace("lastname", doc['lastname'].title() )
			building = building.replace("insertfacenum", str( k + 1 ) ).replace("insertfacetotal", str( totalFaces ) )
			building = building.replace( "insertlenses", doc['face'][k]['attribute']['glass']['value'] + " Confidence: " + str( doc['face'][k]['attribute']['glass']['confidence'] ) )
			building = building.replace( "insertsex", doc['face'][k]['attribute']['gender']['value'] + " Confidence: " + str( doc['face'][k]['attribute']['gender']['confidence'] ) )
			building = building.replace( "talksex", doc['face'][k]['attribute']['gender']['value'] )
			building = building.replace( "talkskin", doc['face'][k]['attribute']['race']['value'] )
			building = building.replace( "insertskin", doc['face'][k]['attribute']['race']['value'] + " Confidence: " + str( doc['face'][k]['attribute']['race']['confidence'] ) )
			building = building.replace( "insertage", str( doc['face'][k]['attribute']['age']['value'] ) )
			if doc['face'][k]['attribute']['smiling']['value'] > 60:
				decision = "Yes"
			else:
				decision = "No"
			if ( smiling and decision != smiling ):
				continue
			final = final + building.replace( "insertlink" , doc['link'] ).replace( "insertemotion", decision + " Value: " + str( doc['face'][k]['attribute']['smiling']['value'] ) )
	return final

try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    print("")
    filestr = """
<!DOCTYPE HTML>
<html>
<head>
	<title>FaceCapture</title>
	<script src="http://162.249.2.138/style/voice.js"></script>
	<link rel="stylesheet" type="text/css" href="http://162.249.2.138/style/astyle.default.css">
	<link rel="stylesheet" type="text/css" href="http://162.249.2.138/style/apager.css">
	<style>
	.photograph {
		width: 100%;
	}

	.photocontainer{
		width: 200px;
	}

	.centertext{
		text-align: center;
	}

	.photoinfo{
		vertical-align: text-top;
	}

	#phototable{
		margin-left: auto;
		margin-right: auto;
		margin-top: 30px;
		width: 80%;
	}
	</style>

	<script language="javascript">

	function toggleSidebar() {
		if(document.getElementById("sidebar").style.display == "none")
		{
			if(navigator.userAgent.indexOf("MSIE") > -1)
				document.getElementById("sidebar").style.display = "block";
			else
				document.getElementById("sidebar").style.display = "table-cell";
		}
		else 
		{
			document.getElementById("sidebar").style.display = "none";
		}

		document.getElementById("sidestrip").width = 10;

	}

	window.onload=toggleSidebar;
	</script>
</head>

<body>

<table width="100%" id="aheader"><tr>
<td><div id="logo">FaceCapture</div></td>
<td align="right">
<div style="font-size:11px;padding:3px;">
	<span style="font-size:13px;color:#4E9829;font-weight:bold;"></span>
</div>
</td>
</tr></table>


<table border="0" cellspacing="0" cellpadding="0" width="100%" id="maintable">

<tr>

<td valign="top" id="sidestrip" width="10" align="center" onclick="javascript:toggleSidebar()">
<span id="togglemenu">&bull;<br>&bull;<br>&bull;<br>&bull;<br>&bull;<br>&bull;<br>&bull;<br>&bull;<br>&bull;<br>&bull;<br></span>
</td>


<td valign="top" width="130" id="sidebar" rowspan="2" style="display:none;">

<div class="menus">

<table border="0" cellspacing="1" cellpadding="2" class="menu" width="100%">

	<tr><td class="menucell"><a href="http://162.249.2.138/uploader/index.php">Upload A Photo</a></td></tr>

	<tr><td class="menuhead">Categories</td></tr>
	<tr><td class="menucell"><a href="?category=Uploads" class="menulink">Uploads</a></td></tr>
	<tr><td class="menucell"><a href="?category=Presidents" class="menulink">Presidents</a></td></tr>


	<tr><td class="menuhead">Celebrities</td></tr>
		insertceleblist

</table>

</div>

</td>

<td valign="top" id="main">

<h2>insertfirstname insertlastname insertcategory</h2>

<form class="box" action="" method="get">

	<input type="hidden" name="firstname" value="insertfirstname" />
	<input type="hidden" name="lastname" value="insertlastname" />
	<input type="hidden" name="category" value="insertcategory" />

	<table id="searchform" cellspacing="5">
		<tr>		
			<td>Smiling:</td> 
			<td>
				<select name="smiling">
					<option value="">- All -</option>
					<option value="Yes" >Yes</option>
					<option value="No" >No</option>
				</select>
			</td>

			<td>Glasses:</td>
			<td>
				<select name="glasses">
					<option value="">- All -</option>
					<option value="Normal" >Yes</option>
					<option value="None" >No</option>
				</select>
			</td>

			<td> Skin Color: </td>

			<td> 
				<select name="skin">
					<option value="">- All -</option>
					<option value="Asian">Asian</option>
					<option value="Black">Black</option>
					<option value="White">White</option>
				</select>
			</td>

			<td> Gender: </td>

			<td> 
				<select name="gender">
					<option value="">- All -</option>
					<option value="Female">Female</option>
					<option value="Male">Male</option>
				</select>
			</td>

		</tr>
		<tr>
			<td>&nbsp;</td>
			<td colspan="3"> 
				<button type="submit">&nbsp;Go&nbsp;</button>
				<button type="button" onclick="location.href='?';">View All</button>
			</td>
		</tr>
	</table>

</form>

<div><span class="rescount">insertsize</span> matching results in this view</div>

<form method="post" action="" name="frmAds">
<table id="phototable" cellpadding="6" cellspacing="1" class="grid">
	<tr>
		<td class="gridhead photocontainer centertext">Photograph</td>
		<td class="gridhead centertext"> Analysis </td>
	</tr>

		replacethis

</table>
</form>
</td>
</tr>
</table>
</body>
</html>
"""
    filestr = filestr.replace("replacethis", main() ).replace( "insertsize", str( dataset.count() ) ).replace("insertceleblist", getCelebList() )
    filestr = filestr.replace("insertfirstname", firstname ).replace("insertlastname", lastname ).replace("insertcategory", category)

    print filestr

except:
    cgi.print_exception()                 # catch and print errors
