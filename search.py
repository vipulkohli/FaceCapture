#!/usr/bin/env python2.7

import cgi   # NEW
import pymongo

db = pymongo.MongoClient().faces.entries

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
firstname = form.getvalue('firstname')
lastname  = form.getvalue('lastname')
glasses  = form.getvalue('glasses')
skin  = form.getvalue('skin')
smiling = form.getvalue('smiling')
target = {}
if( firstname and lastname ):
	target = {"firstname":firstname, "lastname" : lastname}
dataset = db.find( target )

def main():
    wrapper = """ 
	<tr class="gridcell">

		<td> <img class="photograph" src="insertlink" />	 </td>

		<td class="photoinfo" >
		firstname lastname
		<ul>
			<li>Smiling: insertemotion</li>
			<li>Goggles: insertlenses</li>
			<li>Gender: insertsex</li>
			<li>Skin: insertskin</li>
			<li>Age: insertage</li>
		</ul>
		</td>

	</tr>
    """    
    final = ""
    for doc in dataset:
	for k in range( 0, len(doc['face']) ):
		if( glasses and doc['face'][k]['attribute']['glass']['value'] != glasses ):
			continue
		if( skin and doc['face'][k]['attribute']['race']['value'] != skin ):
			continue
		building = wrapper.replace("firstname", doc['firstname'].title() ).replace("lastname", doc['lastname'].title() )
		building = building.replace( "insertlenses", doc['face'][k]['attribute']['glass']['value'] )
		building = building.replace( "insertsex", doc['face'][k]['attribute']['gender']['value'] )
		building = building.replace( "insertskin", doc['face'][k]['attribute']['race']['value'] )
		building = building.replace( "insertage", str( doc['face'][k]['attribute']['age']['value'] ) )
		if doc['face'][k]['attribute']['smiling']['value'] > 60:
			decision = "Yes"
		else:
             		decision = "No"
		if ( smiling and decision != smiling ):
				continue
             	final = final + building.replace( "insertlink" , doc['link'] ).replace( "insertemotion", decision )
    return final

try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    print("")
    filestr = """
<!DOCTYPE HTML>
<html>
<head>
<title>FaceCapture</title>
<link rel="stylesheet" type="text/css" href="http://162.249.2.138/style/astyle.default.css">
<link rel="stylesheet" type="text/css" href="http://162.249.2.138/style/apager.css">
<style>
.photograph {
	width: 100%;
}

.photocontainer{
	width: 40%;
}

.centertext{
	text-align: center;
}

.photoinfo{
	vertical-align: text-top;
}

#phototable{
	margin: auto;
	width: 80%;
}
</style>
</head>


<script language="javascript">
function toggleSidebar()
{
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

function toggleSuggest()
{
	var suggestbox = document.getElementById("suggestbox");
	if(suggestbox.style.display == "none")
	{
			suggestbox.style.display = "block";
	}
	else 
	{
			suggestbox.style.display = "none";
	}

}
</script>


<body>

<table width="100%" id="aheader"><tr>
<td><div id="logo">FaceCapture</div></td>
<td align="right">
<div style="font-size:11px;padding:3px;">
<span style="font-size:13px;color:#4E9829;font-weight:bold;"></span>

<b></a></b>
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
<tr><td class="menuhead">Celebrities</td></tr>
<tr><td class="menucell"><a href="?firstname=drake&lastname=bell" class="menulink">Drake Bell</a></td></tr>
</table>

</div>

</td>

<td valign="top" id="main">

<h2>Drake Bell</h2>

<form class="box" action="" method="get">

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

<div><span class="rescount">insertsize</span> mathcing results in this view</div>

<br>

<div class="legend" align="right"><b>V</b> - Verified &nbsp; <b>A</b> - Approved</div>
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
</div>
</body>
</html>
"""
    filestr = filestr.replace("replacethis", main() ).replace( "insertsize", str( dataset.count() ) )
    print filestr

except:
    cgi.print_exception()                 # catch and print errors
