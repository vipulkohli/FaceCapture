<!DOCTYPE HTML>
<html>
<head></head>
<body>
<form action="index.php">
<input type="submit" value="Go Back" />
</form>
<form action="http://162.249.2.138/cgi-bin/index.py">
<input type="submit" value="Go Home" />
</form>
<?php
$filename = "";
$firstname = $_POST["firstname"];
$lastname = $_POST["lastname"];
if ($_FILES["file"]["error"] > 0) {
  echo "Error: " . $_FILES["file"]["error"] . "<br>";
}
else {
	echo "<img width = '200' height = '200' src='upload/" . $_FILES["file"]["name"] ."' /><br><br><br><br>";
	echo "Upload: " . $_FILES["file"]["name"] . "<br>";
	echo "Type: " . $_FILES["file"]["type"] . "<br>";
	echo "Size: " . ($_FILES["file"]["size"] / 1024) . " kB<br>";
	echo "Stored in: " . $_FILES["file"]["tmp_name"];
}

$okTypes = array( "image/gif", "image/jpeg", "image/jpg", "image/pjpeg", "image/x-png", "image/png");
$proposedType = $_FILES["file"]["type"];

if( ! in_array( $proposedType, $okTypes ) )
	die( "Invalid file type" );

if ($_FILES["file"]["error"] > 0) {
    echo "Return Code: " . $_FILES["file"]["error"] . "<br>";
}
else{
	echo "Upload: " . $_FILES["file"]["name"] . "<br>";
	echo "Type: " . $_FILES["file"]["type"] . "<br>";
	echo "Size: " . ($_FILES["file"]["size"] / 1024) . " kB<br>";
	echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br>";
	
	if (file_exists("upload/" . $_FILES["file"]["name"])){
		echo $_FILES["file"]["name"] . " already exists. ";
	}
	else{
		$filename = $_FILES["file"]["name"];
		move_uploaded_file($_FILES["file"]["tmp_name"], "upload/" . $_FILES["file"]["name"]);
      		echo file_get_contents("http://162.249.2.138/cgi-bin/upload.py?filename=$filename&firstname=$firstname&lastname=$lastname" );	
	}
}

?>
</body>
</html>